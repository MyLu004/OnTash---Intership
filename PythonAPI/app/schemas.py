from pydantic import BaseModel
from datetime import datetime


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

    class Config:
        orm_mode = True


