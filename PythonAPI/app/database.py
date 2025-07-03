from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from psycopg2.extras import RealDictCursor




from .config import SQLALCHEMY_DATABASE_URL
#specify the database URL



#SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

#specify the database URL


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



# FOR REFENRECE
# while True:
#     #try to connect to the database
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             database="fastapi", 
#             user = "postgres", 
#             password="2004", 
#             cursor_factory=RealDictCursor)
#         print(RealDictCursor)
        
#         cursor  = conn.cursor()
#         print("Database connection successful, yipppeee!")
#         break  #exit the loop if connection is successful
#     #if connection fails, print the error and try again
#     except Exception as error:
#         print("Database connection failed")
#         print("Error:", error)
#         time.sleep(2)  #wait for 2 seconds before trying again