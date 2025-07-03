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
### What I Learned
- JWT (JSON Web Token) : to securely encode user identify and expiration  

- OAuth2PasswordRequestForm : for parsing login credentials from `x-www-form-urlencoded` input  

- OAuth2PasswordBearer : for protecting routes and auto-extracting tokens from Authorization headers  

- FastAPI Depends() : for dependency injection of form data, database sessions, and auth logic

- Postman scripting  : for auto-setting `access_token` after login and reusing it in headers for authenticated routes.

---
### Tech Stack


| Category             | Tool/ Library                               |
| ---------------------| ------------------------------------------- |
|  Backend             | Fast API                                    |
|  Auth                |    `python-jose` (JWT), `OAuth2`, `bearer`  |
|  Password Hashing    |    `passlib[bcrypt]`                        |
|  DB ORM              | SQLAlchemy                                  | 
| Testing Tool         | Postman                                     |


### Authentication Flow
1. User logs in via /login with email & password.

2. FastAPI:
    - Looks up the user by email.

    - Verifies the password hash with passlib.

    - If valid, creates a JWT with reader_id and expiration.

    - Returns the token and token_type = "bearer".
3. Cleint stores the token
4. To access protected endpoints, client adds:  
``` 
Authorization: Bearer <token>
```

5. FastAPI uses get_current_reader() to:

    - Decode and verify token.

    - Load the reader from the DB using reader_id.

## 📁 Folder Structure Overview

``` 
app/
├── routes/
│   ├── auth.py         # Login route using OAuth2
│   ├── books.py        # Protected book endpoints
│   └── reader.py       # User registration and retrieval
├── oauth2.py           # Token creation, verification, and user auth
├── utils.py            # Password hashing and verification
├── database.py         # DB setup and session handling
├── schemas.py          # Pydantic models for request/response
├── models.py           # SQLAlchemy ORM models
└── main.py             # FastAPI app instance and router includes
```

## EXAMPLE
Login:
- Method: `POST`
- URL: `/login`
- Body: `x-www-form-urlencoded`      
  
 
``` 
username: email@example.com
password: yourpassword
```

Token Auto-Extraction in Postman Tests Tab:
```javascript 
const res = pm.response.json(); pm.environment.set("access_token", res.access_token);
```

Authorization Header for protected routes
```
Authorization: Bearer {{access_token}}
```

---
## 🔗 RESOURCE
- [Study JWT](https://youtu.be/7Q17ubqLfaM)
- [FastAPI Security Documentation](https://fastapi.tiangolo.com/tutorial/security/ ) 
- [OAuth2 with Password and hasing]( https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/)


## Author
**My Lu**  
Intern @ Ontash  
Email: myluwork004@gmail.com
LinkedIn : www.linkedin.com/in/my-lu  
Github : https://github.com/MyLu004 
