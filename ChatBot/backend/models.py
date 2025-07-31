from  database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
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



class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    messages = relationship("Message", back_populates="chat")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    role = Column(String)
    text = Column(Text)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    chat = relationship("Chat", back_populates="messages")
