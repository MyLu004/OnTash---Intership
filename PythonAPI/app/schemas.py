from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

from typing import Optional





# == USER SCHEMAS ==
class UserOut(BaseModel):
    id: int
    email: EmailStr
    create_at: datetime  #using str for datetime, can be changed to datetime if needed

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# == POST SCHEMAS ==
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  #default value is True
    

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class Post(PostBase):
    id : int
    create_at: datetime  #using str for datetime, can be changed to datetime if needed
    owner_id: int  #owner_id is the id of the user who created the post
    owner : UserOut
    class Config:
        orm_mode = True


class PostOut(BaseModel):
    post: Post
    votes : int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    pass


# == TOKEN SCHEMAS ==
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] | None = None  #id can be None if not provided, using union type for optional id
    email: EmailStr | None = None  #email can also be None if not provided, using union type for optional email


class Vote(BaseModel):
    post_id: int
    #user_id: int

    dir : conint (le=1)

    class Config:
        orm_mode = True

class VoteOut(Vote):
    pass