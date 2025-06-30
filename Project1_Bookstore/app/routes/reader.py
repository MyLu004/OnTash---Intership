from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import get_db
from typing import List



router = APIRouter(
    prefix="/reader",  # set a prefix for all routes in this router
    tags=["Reader"]  # set a tag for the router, useful for documentation
)  # create a router for reader related operations


#CRUD OPERATION FOR READERS STORE API


# Get all reader
@router.get("/", response_model=List[schemas.ReaderOut])
def get_readers(db: Session = Depends(get_db)):
    """
    Get all books from the bookstore.
    """
    readers = db.query(models.Reader).all()
    return readers

#get reader by ID
@router.get("/{reader_id}", response_model=schemas.ReaderOut)
def get_reader(reader_id: int, db: Session = Depends(get_db)):
    """
    Get a reader by ID.
    """
    reader = db.query(models.Reader).filter(models.Reader.id == reader_id).first()
    if reader is None:
        raise HTTPException(status_code=404, detail=f"Reader with id {reader_id} not found")
    
    return reader

#create/add new reader
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ReaderOut)
def create_reader(reader: schemas.ReaderCreate, db: Session = Depends(get_db)):
    """
    Create a new reader.
    """

    #hasing reader password to storing in the database for security
    hashed_password = utils.hash(reader.password)  # Uncomment if you have a hashing utility

    reader.password = hashed_password  # Assign the hashed password to the reader object

    new_reader = models.Reader(**reader.dict())
    db.add(new_reader)
    db.commit()
    db.refresh(new_reader)

    return new_reader

