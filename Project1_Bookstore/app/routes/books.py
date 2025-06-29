#file to handing the routing for the books
# File: Project1_Bookstore/app/main.py
# Project 1 Bookstore API

#Project 1 Bookstore API : requirements
# 1. Create a book
# 2. Get all books
# 3. Get a book by ID
# 4. Update a book by ID
# 5. Delete a book by ID

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/books",  # set a prefix for all routes in this router
    tags=["Books"]  # set a tag for the router, useful for documentation
)


#CRUD OPERATION FOR BOOKS STORE API


#get all the books
@router.get("/", response_model=List[schemas.BookOut])
def get_books(db: Session = Depends(get_db), curr_reader: int = Depends(oauth2.get_current_reader)):
    books = db.query(models.Book).all()
    return books

#get a book by ID
@router.get("/{book_id}",response_model=schemas.BookOut)
def get_book(book_id: int, db: Session = Depends(get_db), curr_reader: int = Depends(oauth2.get_current_reader)):
    books = db.query(models.Book).filter(models.Book.id == book_id).first()
    if books is None:
        raise HTTPException(status_code=404, detail= f"Book id {book_id} not found to get")
    
    return books


# create/add new book
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.BookOut)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db), curr_reader: int = Depends(oauth2.get_current_reader)):

    new_books = models.Book(owner_id = curr_reader.id,**book.dict())
    db.add(new_books)
    db.commit()
    db.refresh(new_books)

    return new_books

# update a book by ID
@router.put("/{book_id}")
def update_book(book_id: int, book: schemas.BookBase, db: Session = Depends(get_db), curr_reader: int = Depends(oauth2.get_current_reader)):
    book_query = db.query(models.Book).filter(models.Book.id == book_id)
    book_data = book_query.first()

    if not book_data:
        raise HTTPException(status_code=404, detail=f"Book {book_id} not found to update")
    
    book_query.update(book.dict(), synchronize_session=False)
    db.commit()

    return book_query.first()


#delete a book by ID
@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db), curr_reader: int = Depends(oauth2.get_current_reader)):
    delete_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    
    
    if delete_book is None:
        raise HTTPException(status_code=404, detail=f"Book {book_id} not found to delete")

    db.delete(delete_book)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
