from  .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql import text

from sqlalchemy.orm import relationship

#Base = declarative_base()

class User(Base):
    __tablename__ = "users"  #specify the table name

    id = Column(Integer, primary_key=True, nullable=False)  #define the id column as an integer and primary key
    email = Column(String, nullable=False, unique=True)  #define the email column as a string, not nullable, and unique
    password = Column(String, nullable=False)  #define the password column as a string and not nullable
    create_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)  #define the create_at column as a timestamp with a default value of the current time
