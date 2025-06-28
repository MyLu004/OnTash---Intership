from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import models, schemas, database
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  # OAuth2 scheme for token authentication

# 3 token settings
#SECRET_KEY
#ALGORITHM
#ACCESS_TOKEN_EXPIRE_MINUTES 



SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict):
    """
    Create a JWT access token.
    
    Args:
        data (dict): The data to encode in the token.
        expires_delta (timedelta | None): The expiration time for the token.
        
    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    """
    Verify a JWT access token.
    
    Args:
        token (str): The JWT token to verify.
        
    Returns:
        dict: The decoded token data if verification is successful.
        
    Raises:
        JWTError: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id:str = payload.get("user_id") # Ensure 'users_id' is in the payload

        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id=id)

        #return payload
    except JWTError as e:
        raise credentials_exception
    
    return token_data  # Return the token data if verification is successful


#extract the id for us
def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(database.get_db)):
    """
    Get the current user from the JWT token.
    
    Args:
        token (str): The JWT token to decode.
        
    Returns:
        schemas.TokenData: The token data containing user information.
        
    Raises:
        credentials_exception: If the token is invalid or expired.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()  # Fetch the user from the database using the ID from the token
    if user is None:
        raise credentials_exception
    
    # If the user exists, return the token data
    return user