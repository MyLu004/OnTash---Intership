from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, utils, oauth2
from ..database import get_db

from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(
    tags=["Authentication"]  # set a tag for the router, useful for documentation
)  # create a router for authentication related operations


@router.post("/login", response_model=schemas.Token)  # set the response model to Token schema
def login(reader_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login endpoint.
    This is a placeholder for the login functionality.
    """
    # Here you would typically verify the user's credentials and return a token
    # For now, we will just return a success message
    reader = db.query(models.Reader).filter(models.Reader.email == reader_credentials.username).first()
    
    if not reader:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )
    
    if not utils.verify(reader_credentials.password, reader.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )

    access_token = oauth2.create_access_token(data={"reader_id": reader.id})

    
    return {"access_token": access_token, "token_type": "bearer"}