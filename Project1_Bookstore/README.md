# 📚 Bookstore API – Project 1

**Author**: My Lu  
**Date**: June 26, 2025  
**Tech Stack**: FastAPI, PostgreSQL, SQLAlchemy, Postman  

---

This is a RESTful API built using **FastAPI** and **SQLAlchemy** to manage a digital bookstore. It supports full CRUD (Create, Read, Update, Delete) operations for books stored in a PostgreSQL database.

- [Demo Video](https://www.loom.com/share/97f5eacf27344f089c52a5fa96625595?sid=001f325f-e2a0-4c0c-808f-f1255906d7d8)
- [Project Report](https://docs.google.com/document/d/1iR3qdNHw-duEsGRtgcEELMojaHSQxMDW93NZwPv6Euc/edit?usp=sharing)
---

## 🚀 Features

- Create a new book
- Get a list of all books
- Get a book by ID
- Update a book by ID
- Delete a book by ID
- PostgreSQL database integration
- Environment variable support via `.env`
- Schema validation using Pydantic
- ORM modeling using SQLAlchemy

---
## 📁 Project Structure


``` 
Project1_Bookstore/
│
├── app/
│   ├── main.py            # FastAPI app and route definitions
│   ├── database.py        # SQLAlchemy DB setup and session management
│   ├── models.py          # ORM models for the database
│   └── schemas.py         # Pydantic schemas for validation and response
│
├── .env                   # Database credentials (not committed to Git)
├── .gitignore             # Git ignore rules
├── requirements.txt       # Project dependencies
└── README.md              # README file [this]
```

## ⚙️ Requirements

- Python 3.8+
- PostgreSQL
- `pip install -r requirements.txt`

## 🔐 .env File Format

Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bookstore
DB_USER=your_db_user
DB_PASSWORD=your_db_password
```

## HOW IT WOKR

### 📦 Models (models.py)
Defines a  `Book` model mapped to the `bookstore` table with fields like `id`, `title`, `content`, `genres`, `published`, and `create_at`

### 🧱 Database (database.py)
- Connects to PostgreSQL using environment variables
- Configures the SQLAlchemy engine and session maker
- Provides a get_db() dependency for route injection

### 🛡️ Schemas (schemas.py)
- Use Pydantic to validate incoming data and control the surface of API response

## API Rooutes [`main.py`]
5 main CRUD endpoint:
- `GET/books` : get all the book
- `GET/books/{book_id}` : get a book by ID
- `POST/books` : create a new book
- `PUT/books/{book_id}`: update an exisiting book
- `DELETE/books/{book_id}`:delete a book

## HOW TO RUN THE APP
<pre lang='bash'>
    <code>
    uvicorn app.main:app --reload
    </code>
</pre>

- Visit the localhost url : http://127.0.0.1:8000/docs 
- To view the UI or paste the url in the postman to do the API request

## FUTURE IMPROVEMENT
- Add user authentication
- Implement front end application
- Containerize with Docker

## Author
My Lu  
Intern @ OnStach  
Email: myluwork004@gmail.com  
Github : https://github.com/MyLu004 
