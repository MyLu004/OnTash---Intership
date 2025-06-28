from  .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql import text



'''
NOTE ALONG THE WAY:
- The Post class represents a post in the database.
- The User class represents a user in the database.
- Both classes inherit from Base, which is the declarative base class for SQLAlchemy models.

- Foregin keys type should match the type of the primary key in the referenced table.
'''

class Post(Base):
    __tablename__ = "posts"  #specify the table name

    id = Column(Integer, primary_key=True, nullable=False)  #define the id column as an integer and primary key
    title = Column(String, nullable=False)  #define the title column as a string and not nullable
    content = Column(String, nullable=False)  #define the content column as a string and not nullable
    published = Column(Boolean, server_default= 'TRUE', nullable=False)  #define the published column as a boolean with a default value of True
    create_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)  #define the create_at column as a timestamp with a default value of the current time
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, )  #define the owner_id column as an integer and not nullable, this will be used to link the post to the user who created it


class User(Base):
    __tablename__ = "users"  #specify the table name

    id = Column(Integer, primary_key=True, nullable=False)  #define the id column as an integer and primary key
    email = Column(String, nullable=False, unique=True)  #define the email column as a string, not nullable, and unique
    password = Column(String, nullable=False)  #define the password column as a string and not nullable
    create_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)  #define the create_at column as a timestamp with a default value of the current time