
# File: Project1_Bookstore/app/main.py
# Project 1 Bookstore API


#import env for data and information
from dotenv import load_dotenv
import os

from fastapi import FastAPI, status,Response, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel


#import for database connection
from .database import engine, get_db
from sqlalchemy.orm import Session
from . import models, schemas


import time
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List

#create an instance of FastAPI | initialize the database
app = FastAPI()
models.Base.metadata.create_all(bind=engine)

#Project 1 Bookstore API : requirements
# 1. Create a book
# 2. Get all books
# 3. Get a book by ID
# 4. Update a book by ID
# 5. Delete a book by ID

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



#CRUD OPERATION FOR BOOKS STORE API
@app.get("/")
def root():
    return {"message": "Welcome to the Bookstore API!"}


#get all the books
@app.get("/books", response_model=List[schemas.BookOut])
def get_books(db: Session = Depends(get_db)):
    books = db.query(models.Book).all()
    return books

#get a book by ID
@app.get("/books/{book_id}",response_model=schemas.BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    books = db.query(models.Book).filter(models.Book.id == book_id).first()
    if books is None:
        raise HTTPException(status_code=404, detail= f"Book id {book_id} not found to get")
    
    return books


# create/add new book
@app.post("/books", status_code=status.HTTP_201_CREATED, response_model=schemas.BookOut)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):

    new_books = models.Book(**book.dict())
    db.add(new_books)
    db.commit()
    db.refresh(new_books)

    return new_books

# update a book by ID
@app.put("/books/{book_id}")
def update_book(book_id: int, book: schemas.BookBase, db: Session = Depends(get_db)):
    book_query = db.query(models.Book).filter(models.Book.id == book_id)
    book_data = book_query.first()

    if not book_data:
        raise HTTPException(status_code=404, detail=f"Book {book_id} not found to update")
    
    book_query.update(book.dict(), synchronize_session=False)
    db.commit()

    return book_query.first()


#delete a book by ID
@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    delete_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    
    
    if delete_book is None:
        raise HTTPException(status_code=404, detail=f"Book {book_id} not found to delete")

    db.delete(delete_book)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
