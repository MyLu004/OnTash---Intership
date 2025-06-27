from pydantic import BaseModel
from datetime import datetime 


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