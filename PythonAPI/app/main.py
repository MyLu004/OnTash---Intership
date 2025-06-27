from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body

#other external libraries
from pydantic import BaseModel
from typing import Optional, List
from random import randrange

#database connection
import psycopg2
from psycopg2.extras import RealDictCursor

import time

#import the models and database
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)  #create the database tables if they don't exist


#create instance of FastAPI
app = FastAPI()

#create dependency to get a database session


#PATH OPERATIONS / ROUTES
#define a simple route (GET request at "/")
#request GET method url :  "/"
#the order is matters


#define the class Post : https://docs.pydantic.dev/latest/  
#data we want the front end to look like
#title str, content str





while True:
    #try to connect to the database
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi", 
            user = "postgres", 
            password="2004", 
            cursor_factory=RealDictCursor)
        
        cursor  = conn.cursor()
        print("Database connection successful, yipppeee!")
        break  #exit the loop if connection is successful
    #if connection fails, print the error and try again
    except Exception as error:
        print("Database connection failed")
        print("Error:", error)
        time.sleep(2)  #wait for 2 seconds before trying again


my_posts = [
    {"title": "Post 1", "content": "Content of post 1", "id":1},
    {"title": "Post 2", "content": "Content of post 2", "id":2}
]


@app.get("/") 
def root():

    #the data get send back to the client
    return {"message": "Hello World kinoko from FastAPI! :3"}

@app.get("/posts", response_model=list[schemas.Post])  #set the response model to a list of Post schema
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()  #get all posts from the database using SQLAlchemy ORM
    #print(posts)  #print the posts to the console
    return posts



# db: Session = Depends(get_db) : allow us to use the database session in the function
# Depend is a way to declare dependencies in FastAPI, allowing us to use the database session in the function

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)  #set the status code to 201 Created
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # #the order is matters 
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #     (post.title, post.content, post.published)
    # )

    # new_post = cursor.fetchone()  #fetch the newly created post
    # conn.commit()  #commit the changes to the database

    new_posts = models.Post(**post.dict())  #create a new post object
     
    db.add(new_posts)  #add the new post to the database session
    db.commit()  #commit the changes to the database
    db.refresh(new_posts)  #refresh the new post object to get the updated data from the database
    
    return new_posts 

@app.get("/posts/{id}", response_model=schemas.Post)  #set the response model to Post schema
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    #get a post by id
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))  #execute the query to get the post by id
    # posts = cursor.fetchone()  #fetch the post from the database
    posts =  db.query(models.Post).filter(models.Post.id == id).first()  #use SQLAlchemy ORM to get the post by id
    
    if posts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )

    return posts



#delete a post by id
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()  #fetch the deleted post
    # conn.commit()

    delete_post = db.query(models.Post).filter(models.Post.id == id).first() #get the post to be deleted


    if delete_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id {id} not found"
        )
    db.delete(delete_post)  #delete the post from the database session
    db.commit()  #commit the changes to the database


    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}", response_model=schemas.PostUpdate)  #set the response model to Post schema    
def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):

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

    post_query.update(post.dict(), synchronize_session=False)  #update the post in the database session
    db.commit()  #commit the changes to the database
    
    return post_query.first()  #return the updated post

