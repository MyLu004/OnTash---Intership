from fastapi import APIRouter, Depends, HTTPException, status, APIRouter, Response
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from .. import oauth2
from typing import List, Optional


router = APIRouter(
    prefix="/posts",  #set a prefix for all routes in this router
    tags=["Posts"]  #set a tag for the router, useful for documentation
)  #create a router for post related operations

#@router.get("/", response_model=list[schemas.Post])  #set the response model to a list of Post schema
@router.get("/", response_model=list[schemas.PostOut])  #set the response model to a list of Post schema
def get_posts(db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search : Optional[str] =""):
    # posts = db.query(models.Post).filter(models.Post.owner_id == curr_user.id).all()  #get all posts from the database using SQLAlchemy ORM
    #print(posts)  #print the posts to the console

    #posts = db.query(models.Post).all()  #get all posts from the database using SQLAlchemy ORM

    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()  #get a limited number of posts from the database using SQLAlchemy ORM with pagination

    get_posts = db.query(models.Post, func.count(models.Vote.post_id).label("vote")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter= True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    #print(get_posts)

    #return [{"Post": post, "votes": vote} for post, vote in result]

    return [{"post": post, "votes": vote} for post, vote in get_posts]




@router.get("/{id}", response_model=schemas.PostOut)  #set the response model to Post schema
def get_post(id: int, response: Response, db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)):
    #get a post by id
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))  #execute the query to get the post by id
    # posts = cursor.fetchone()  #fetch the post from the database
    
    #posts =  db.query(models.Post).filter(models.Post.id == id).first()  #use SQLAlchemy ORM to get the post by id
    
    posts, votes = db.query(models.Post, func.count(models.Vote.post_id).label("vote")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter= True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if posts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )
    
    # if posts.owner_id != curr_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Not authorized to perform requested action"
    #     )  #check if the current user is the owner of the post

    return {"post": posts, "votes": votes}


# db: Session = Depends(get_db) : allow us to use the database session in the function
# Depend is a way to declare dependencies in FastAPI, allowing us to use the database session in the function

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)  #set the status code to 201 Created
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)):
    # #the order is matters 
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #     (post.title, post.content, post.published)
    # )

    # new_post = cursor.fetchone()  #fetch the newly created post
    # conn.commit()  #commit the changes to the database
    
    print("current user id",curr_user.id)  #print the current user's email to the console
    new_posts = models.Post(owner_id = curr_user.id, **post.dict())  #create a new post object
     
    db.add(new_posts)  #add the new post to the database session
    db.commit()  #commit the changes to the database
    db.refresh(new_posts)  #refresh the new post object to get the updated data from the database
    
    return new_posts 





#delete a post by id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()  #fetch the deleted post
    # conn.commit()

    delete_post = db.query(models.Post).filter(models.Post.id == id).first() #get the post to be deleted


    if delete_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id {id} not found"
        )
    

     #check if the current user is the owner of the post
    if delete_post.owner_id != curr_user.id: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")  #if not, raise an exception

    db.delete(delete_post)  #delete the post from the database session
    db.commit()  #commit the changes to the database

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model=schemas.Post)  #set the response model to Post schema    
def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute(
    #     """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #     (post.title, post.content, post.published, str(id))
    # )

    # updated_post = cursor.fetchone()  #fetch the updated post
    # conn.commit()  #commit the changes to the database


    post_query = db.query(models.Post).filter(models.Post.id == id)

    post_data = post_query.first()  #get the post to be updated



    if post_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Post with id {id} not found"
            )
    
    if post_data.owner_id != curr_user.id: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")  #if not, raise an exception

    post_query.update(post.dict(), synchronize_session=False)  #update the post in the database session
    db.commit()  #commit the changes to the database
    
    return post_query.first()  #return the updated post