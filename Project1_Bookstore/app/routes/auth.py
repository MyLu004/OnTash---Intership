

# MY LU
# 6/29/2025

'''
Project 2 : User and Authentication System
- Create a FastAPI app with
    - /register router that accepts a user and hashes the password
    - /login router that accepts a user and returns a JWT token

- user registration and login functionality
- Use OAuth2PasswordBearer for token authentication
- Use JWT for token creation and verification
- Use SQLAlchemy for database operations
- User Oauth2PasswordRequestForm for login credentials
'''



from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, utils, oauth2
from ..database import get_db

from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(
    tags=["Authentication"]  # set a tag for the router, useful for documentation
)  # create a router for authentication related operations

#handle login functionality and token creation
@router.post("/login", response_model=schemas.Token)  # set the response model to Token schema
def login(reader_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login endpoint.
    This is a placeholder for the login functionality.
    """
    # Here you would typically verify the user's credentials and return a token
    # For now, we will just return a success message
    reader = db.query(models.Reader).filter(models.Reader.email == reader_credentials.username).first()
    
    #check if reader exists
    # If the reader does not exist, raise an HTTPException with a 403 status code
    if not reader:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )
    
    # Verify the password using the utility function
    # If the password does not match, raise an HTTPException with a 403 status code
    if not utils.verify(reader_credentials.password, reader.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )


    #create an access token for the reader
    # This is where you would typically create a JWT token for the authenticated user
    access_token = oauth2.create_access_token(data={"reader_id": reader.id})

    
    return {"access_token": access_token, "token_type": "bearer"}