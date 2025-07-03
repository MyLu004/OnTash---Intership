from  .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql import text

from sqlalchemy.orm import relationship

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
    some_other_column = Column(String, nullable=True)  #example of an additional column, can be removed if not needed

    # Define a relationship with the User model
    # This allows us to access the user who created the post
    owner = relationship("User")  #define a relationship with the User model, this will allow us to access the user who created the post



class User(Base):
    __tablename__ = "users"  #specify the table name

    id = Column(Integer, primary_key=True, nullable=False)  #define the id column as an integer and primary key
    email = Column(String, nullable=False, unique=True)  #define the email column as a string, not nullable, and unique
    password = Column(String, nullable=False)  #define the password column as a string and not nullable
    create_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)  #define the create_at column as a timestamp with a default value of the current time



class Vote(Base):
    __tablename__ = "vote"  #specify the table name

    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)  #define the post_id column as an integer and primary key, this will be used to link the voter to the post they voted for
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)  #define the user_id column as an integer and primary key, this will be used to link the voter to the user who voted

    # Define a relationship with the Post model
    post = relationship("Post")  #define a relationship with the Post model, this will allow us to access the post that was voted for

    # Define a relationship with the User model
    user = relationship("User")  #define a relationship with the User model, this will allow us to access the user who voted