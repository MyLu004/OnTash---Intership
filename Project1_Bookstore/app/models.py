from  .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship


#model for book table in the database
# This class defines the structure of the book table in the database using SQLAlchemy ORM
class Book(Base):
    __tablename__ = "bookstore"  #specify the table name

    id = Column(Integer, primary_key=True, nullable=False)  #define the id column as an integer and primary key
    title = Column(String, nullable=False)  #define the title column as a string and not nullable
    content = Column(String, nullable=False)  #define the content column as a string and not nullable
    published = Column(Boolean, server_default= 'TRUE', nullable=False)  #define the published column as a boolean with a default value of True
    genres = Column(String, nullable=False)  #define the genres column as a string and not nullable
    create_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)  #define the create_at column as a timestamp with a default value of the current time
    owner_id = Column(Integer,ForeignKey("readers.id", ondelete="CASCADE") ,nullable=False)  #define the owner_id column as an integer and not nullable, this will be used to link the book to the reader who created it

    owner = relationship("Reader")


#model for reader table in the database
# This class defines the structure of the reader table in the database using SQLAlchemy ORM
class Reader(Base):
    __tablename__ = "readers"  #specify the table name

    id = Column(Integer, primary_key=True, nullable=False)  #define the id column as an integer and primary key
    
    email = Column(String, nullable=False, unique=True)  #define the email column as a string, not nullable, and unique
    password = Column(String, nullable=False)  #define the password column as a string and not nullable
    
    create_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)  #define the create_at column as a timestamp with a default value of the current time


class Vote(Base):
    __tablename__ = "vote"  #specify the table name

    book_id = Column(Integer, ForeignKey("bookstore.id", ondelete="CASCADE"), primary_key=True)  #define the post_id column as an integer and primary key, this will be used to link the voter to the post they voted for
    reader_id = Column(Integer, ForeignKey("readers.id", ondelete="CASCADE"), primary_key=True)  #define the user_id column as an integer and primary key, this will be used to link the voter to the user who voted

    # Define a relationship with the Post model
    post = relationship("Book")  #define a relationship with the Book model, this will allow us to access the post that was voted for

    # Define a relationship with the User model
    user = relationship("Reader")  #define a relationship with the Reader model, this will allow us to access the user who voted