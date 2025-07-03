from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session  

from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(    prefix="/vote",  # set a prefix for all routes in this router
    tags=["Vote"]  # set a tag for the router, useful for documentation
)  #create a router for vote related operations



@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)):
    """
    Cast a vote for a post.
    
    Args:
        vote (schemas.Vote): The vote data containing post_id and direction.
        db (Session): The database session.
        curr_user (int): The current authenticated user ID.
        
    Raises:
        HTTPException: If the post does not exist or if the user tries to vote on their own post.
        
    Returns:
        dict: A message indicating the vote was cast successfully.
    """
    
    # Check if the post exists
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {vote.post_id} does not exist."
        )

    # Check if the user is trying to vote on their own post
    if post.owner_id == curr_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot vote on your own post."
        )

    # Handle voting logic
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id,
        models.Vote.user_id == curr_user.id
    )

    found_vote = vote_query.first()

    if vote.dir == 1:
        # If the vote direction is 1, add a new vote if it doesn't exist
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {curr_user.id} have already voted on this post {vote.post_id}."
            )
        new_vote = models.Vote(post_id=vote.post_id, user_id=curr_user.id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {"message": "Vote added successfully."}
   
    else:
        # If the vote direction is 0, remove the vote if it exists
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vote for post {vote.post_id} by user {curr_user.id} does not exist."
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote removed successfully."}

