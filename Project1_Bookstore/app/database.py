from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
import os


load_dotenv()
#specify the database URL

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"



engine = create_engine(SQLALCHEMY_DATABASE_URL) 

#create a session local class that will be used to create sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#define the base class for declarative models
Base = declarative_base()


def get_db():
    db = SessionLocal()  #create a new session
    try:
        yield db
    finally:
        db.close()