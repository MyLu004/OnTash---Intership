#for user security
from passlib.context import CryptContext


#hashing security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  #create a password context for hashing passwords

def hash(password: str) -> str:
    """
    Hash a password using bcrypt.
    """
    return pwd_context.hash(password)  #hash the password using bcrypt



def verify(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)  #verify the plain password against the hashed password
