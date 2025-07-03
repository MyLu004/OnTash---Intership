# 📚 Project 3 : Relationships & Authorization

**Author**: My Lu  
**Date**: July 3, 2025  
**Tech Stack**: 


### 📌 Overview
This project implements a full feature **Voting System API** using **FastAPI** and **PostgreSQL** 
- CRUD for books
- Vote (like) on books (once per reader)
- Track total vote counts per books
- Enforce that only the **book owner** can update or delete the book 


- [Demo Video]()
- [Project Report](https://docs.google.com/document/d/1fOFSbPFd767ILrwKZC0wSJikoSD7kNX7QSBec4XpKZU/edit?usp=sharing)

## ⚙️ Technologies Used

- **FastAPI** – Web framework for building APIs quickly
- **SQLAlchemy** – ORM for database interaction
- **PostgreSQL** – Relational database for storing users, posts, and votes
- **Pydantic** – For data validation and serialization
- **Postman** – API testing
- **dotenv** – For managing environment variables
- **Alembic** – (optional) For database migrations

---

## 📁 Features

### ✅ Voting Functionality
- Users can like/vote on a post **only once**.
- Users **cannot vote** on their own post.
- Duplicate votes are **blocked** with appropriate error responses.
- Votes can be **removed** by the user.

### 🔐 Post Ownership
- Users can only **update** or **delete** their own posts.
- Unauthorized actions return 403 Forbidden errors.

### 📊 Optimized Queries
- Vote counts per post are retrieved using:
  - `JOIN` with the votes table
  - `func.count()` and `group_by()` for aggregation
- Includes **pagination**, **limit**, **skip**, and **search** filtering via query parameters.

---
## 📄 API Endpoints Overview

### 🔓 Auth (JWT Token-based)
- `POST /login`: Authenticate and get access token

### 📚 Posts
- `GET /posts`: List all posts with vote counts (supports search, limit, skip)
- `GET /posts/{id}`: Get a single post by ID with vote count
- `POST /posts`: Create a new post (auth required)
- `PUT /posts/{id}`: Update a post (owner only)
- `DELETE /posts/{id}`: Delete a post (owner only)

### 👍 Voting
- `POST /vote`: Like/unlike a post
  - Requires: `book_id`, `dir` (1 to like, 0 to unlike)
  - Handles errors for duplicate votes, non-existent posts, and self-votes


## 📁 Folder Structure Overview

``` 
app/
├── routes/
│   ├── auth.py         # Login route using OAuth2
│   ├── books.py        # Protected book endpoints
│   ├── reader.py       # User registration and retrieval
│   └── vote.py         # Vote functionality
├── oauth2.py           # Token creation, verification, and user auth
├── utils.py            # Password hashing and verification
├── database.py         # DB setup and session handling
├── schemas.py          # Pydantic models for request/response
├── models.py           # SQLAlchemy ORM models
└── main.py             # FastAPI app instance and router includes
```

---
## 🔑 Environment Variables

Add a `.env` file to the root directory with the following variables:

```
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_db_name

```




## GETITNG STARTED
1. **Clone the Repo**:
``` bash 

git clone https://github.com/your-username/voting-api.git
cd voting-api
```

2. **Set up virtual enviroment**
``` bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

3. **Install dependencies**
``` bash
pip install -r requirements.txt
```

4. **Run the API**
``` bash 
uvicorn app.main:app --reload

```

---
## What I Leanred:
- Validating ownership and access control
- Building voting systems with unique constraints and composite keys.
- Performing JOINs and aggregations with SQLAchemy
- Desinging scalable and RESTful API end points
- Using Postman for API test
-- Structing a FastAPI project into modular routers and services



## Author
**My Lu**  
Intern @ Ontash  
Email: myluwork004@gmail.com  
LinkedIn : www.linkedin.com/in/my-lu  
Github : https://github.com/MyLu004 
