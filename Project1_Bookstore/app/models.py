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




#model for reader table in the database
# This class defines the structure of the reader table in the database using SQLAlchemy ORM
class Reader(Base):
    __tablename__ = "readers"  #specify the table name

    id = Column(Integer, primary_key=True, nullable=False)  #define the id column as an integer and primary key
    
    email = Column(String, nullable=False, unique=True)  #define the email column as a string, not nullable, and unique
    password = Column(String, nullable=False)  #define the password column as a string and not nullable
    
    create_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)  #define the create_at column as a timestamp with a default value of the current time