from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List

from fastapi.security import OAuth2PasswordRequestForm


from ..database import get_db
from .. import models, schemas, oauth2

from ..utils import hasing


router = APIRouter(
      # set a prefix for all routes in this router
    tags=["Authentication"]  # set a tag for the router, useful for documentation
)  # create a router for authentication related operations


@router.post("/login", response_model=schemas.Token)  # set the response model to Token schema  
def login(user_credentials: OAuth2PasswordRequestForm = Depends() ,db:Session = Depends(get_db)):
    """
    Login endpoint.
    This is a placeholder for the login functionality.
    """
    # Here you would typically verify the user's credentials and return a token
    # For now, we will just return a success message
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )
    
    if not hasing.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )
    

    access_token = oauth2.create_access_token(data={"sub": user.id})

    #create JWT token
    return {"access_token": access_token, "token_type": "bearer", "email": user.email}

