from fastapi import FastAPI, Response, status, HTTPException, Depends
# from fastapi.params import Body

# #other external libraries
# from pydantic import BaseModel
# from typing import Optional, List
# from random import randrange

# #database connection
# import psycopg2
# from psycopg2.extras import RealDictCursor

from . import models
#import the models and database
from .database import engine
from .routers import post, user, auth, vote

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


app.include_router(post.router)  #include the post router
app.include_router(user.router)  #include the user router
app.include_router(auth.router)  #include the auth router
app.include_router(vote.router)  #include the vote router

@app.get("/") 
def root():

    #the data get send back to the client
    return {"message": "Hello World kinoko from FastAPI! :3"}








