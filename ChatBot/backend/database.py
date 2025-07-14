from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
import os

load_dotenv()
#specify the database URL

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL) 

#create a session local class that will be used to create sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#define the base class for declarative models
Base = declarative_base()


def get_db():
    print("connect succesfful")
    db = SessionLocal()  #create a new session
    try:
        yield db
    finally:
        
        db.close()