from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

from . import models,schemas,database

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


from dotenv import load_dotenv
import os

load_dotenv()

JWT_SECRET= os.getenv("JWT_SECRET")
JWT_ALGORITHM=os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES=os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

#SQLALCHEMY_DATABASE_URL=os.getenv("DATABASE_URL")



def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    
    print("token create")
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        id:str = payload.get("sub") # Ensure 'user_id' is in the payload
        if id is None:
            raise credentials_exception 
        token_data = schemas.TokenData(id=id)

        #return payload
    except JWTError as e:
        raise credentials_exception
    
    return token_data  # Return the token data if verification is successful

