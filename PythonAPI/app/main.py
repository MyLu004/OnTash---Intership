from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body

#other external libraries
from pydantic import BaseModel
from typing import Optional, List
from random import randrange

#database connection
import psycopg2
from psycopg2.extras import RealDictCursor

import time

#import the models and database
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db

from .routers import post, user, auth


models.Base.metadata.create_all(bind=engine)  #create the database tables if they don't exist


#create instance of FastAPI
app = FastAPI()




#create dependency to get a database session


#PATH OPERATIONS / ROUTES
#define a simple route (GET request at "/")
#request GET method url :  "/"
#the order is matters


#define the class Post : https://docs.pydantic.dev/latest/  
#data we want the front end to look like
#title str, content str





while True:
    #try to connect to the database
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi", 
            user = "postgres", 
            password="2004", 
            cursor_factory=RealDictCursor)
        
        cursor  = conn.cursor()
        print("Database connection successful, yipppeee!")
        break  #exit the loop if connection is successful
    #if connection fails, print the error and try again
    except Exception as error:
        print("Database connection failed")
        print("Error:", error)
        time.sleep(2)  #wait for 2 seconds before trying again




app.include_router(post.router)  #include the post router
app.include_router(user.router)  #include the user router
app.include_router(auth.router)  #include the auth router

@app.get("/") 
def root():

    #the data get send back to the client
    return {"message": "Hello World kinoko from FastAPI! :3"}








