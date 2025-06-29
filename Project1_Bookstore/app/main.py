
# File: Project1_Bookstore/app/main.py
# Project 1 Bookstore API

#import env for data and information
from dotenv import load_dotenv
import os

from fastapi import FastAPI

#import for database connection
from .database import engine
from . import models, schemas


import time
import psycopg2
from psycopg2.extras import RealDictCursor



#import the routers
from .routes import books, reader, auth

#create an instance of FastAPI | initialize the database
app = FastAPI()
models.Base.metadata.create_all(bind=engine)



load_dotenv() #load varaible from .env file


DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


while True:
    #try to connect to the database
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME, 
            user = DB_USER, 
            password=DB_PASSWORD, 
            cursor_factory=RealDictCursor)
        
        cursor  = conn.cursor()
        print("Database connection successful, yipppeee!")
        break  #exit the loop if connection is successful
    #if connection fails, print the error and try again
    except Exception as error:
        print("Database connection failed")
        print("Error:", error)
        time.sleep(2)  #wait for 2 seconds before trying again
    

app.include_router(books.router)  #include the books router
app.include_router(reader.router)  #include the reader router
app.include_router(auth.router)  #include the auth router




