from pydantic import BaseModel, EmailStr, conint
from datetime import datetime 



# SCHEMA FOR BOOKS OBJECTS
class BookBase(BaseModel):

    title: str
    content: str
    genres: str
    published: bool = True  # default value is True


class BookCreate(BookBase):
    pass

class BookOut(BookBase):
    id : int
    create_at: datetime  # using str for datetime, can be changed to datetime if needed

    class Config:
        orm_mode = True

#SCHEMA FOR READER OBJECTS
class ReaderBase(BaseModel):
    email: EmailStr
    password: str

class ReaderCreate(BaseModel):
    email: EmailStr
    password: str
   

class ReaderOut(ReaderBase):
    id: int
    create_at: datetime  # using str for datetime, can be changed to datetime if needed

    class Config:
        orm_mode = True



# SCHEMA FOR READER LOGIN | TOKEN
class ReaderLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int | None = None  # id can be None if not provided, using union type for optional id
    email: str | None = None  # email can also be None if not provided, using union type for optional email


class Vote(BaseModel):
    book_id: int
    #user_id: int

    dir : conint (le=1)

    class Config:
        orm_mode = True

class VoteOut(Vote):
    pass