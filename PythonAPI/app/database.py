from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


#specify the database URL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:2004@localhost:5432/fastapi"   


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