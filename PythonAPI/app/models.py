from  .database import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql import text



class Post(Base):
    __tablename__ = "posts"  #specify the table name

    id = Column(Integer, primary_key=True, nullable=False)  #define the id column as an integer and primary key
    title = Column(String, nullable=False)  #define the title column as a string and not nullable
    content = Column(String, nullable=False)  #define the content column as a string and not nullable
    published = Column(Boolean, server_default= 'TRUE', nullable=False)  #define the published column as a boolean with a default value of True
    create_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)  #define the create_at column as a timestamp with a default value of the current time