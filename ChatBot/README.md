
# AI CHATBOT
Author: My Lu  
Date: June 29, 202


### 📌 Overview
An interactive AI chatbot web applicaiton using LLMs (like Llama, GPT, Mistral) with a responsive React frontend and FastAPI backend. Designed to simulate intelligent conversations with support for chat memory, multiple model, and an intuitive UI

- [Demo Video]()
- [Project Report]()

## 📸 Preview
![]()


---
## 🚀 Getting Started
### Prerequisites
- Node.js & npm
- Python 3.11+
- Docker (optional, for deployment)

## How to run the project (if not using docker)

- Backend
```
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt
uvicorn main:app --reload
```

- Front end
```
cd frontend
npm install
npm run dev
```
---
🐳 Docker Deployment

```
docker-compose up --build
```
**Note** : make sure you expose port `5173` (front end) and `8000` (backend)


---
## Project Structure
```

```
---



### Tech Stack
| Category             | Tool/ Library                               |
| ---------------------| ------------------------------------------- |
|   Frontend           | React, TailwindCSS, ReactIcon               |
|   Backend            | FastAPI, Python 3.11, Pydantic, Uvicorn     |
|   LLM                | Ollama, Llamam, Mistral, GPT 3.5, GPT 4     |
|   Database           | SQLAlchemy, PostgresSQL, PgAdmin            | 
|   Deployment         | Dokcet, Docker Compose                      |

---
### ✨ Feature


## Flow Diagrams 
1. 🔐 Authorization Flow
``` javascript
User → [Login Form] → /auth/login → [Token Issued] → Stored in LocalStorage
                         ↓
             JWT/Session validated on each /chat request

```

2. 💬 Chat Flow
``` javascript
[User Types Message]
    ↓
Frontend sends POST → /chat with model, message, and history
    ↓
Backend verifies model + processes request
    ↓
Calls respective LLM API (e.g., Gemini or GPT)
    ↓
Returns response
    ↓
Frontend displays response and updates chat history

```

3. 📤 Send Message Flow (React)

``` javascript
    // handleSend()
    - Prevent default
    - Get message input
    - Append to history
    - Send POST request to /chat
    - Update UI with response
```






---
## 📁 Frontend Structure ( ``` /frontend```)

---
## 📁 Backend Structure ( ``` /backend```)

| File                 | Description                               |
| ---------------------| ------------------------------------------- |
|   `main.py`           | Main FastAPI app file. CORS Middleware, mounts routes   |
|   `routes/chat.py`            | Chat endpoint logic - handles `/chat` POST requests     |
|   `routes/auth.py`                | Ollama, Llamam, Mistral, GPT 3.5, GPT 4     |
|   `routes/process_file.py`           | SQLAlchemy, PostgresSQL, PgAdmin            | 
|   `routes/upload.py`         | Dokcet, Docker Compose                      |
|   `rotes/user.py`     |                                  |
| `models.py`| |
| `oauth2.py`|    |
| `schemas.py`| |



---
### Database
| Category             | Tool/ Library                               |
| ---------------------| ------------------------------------------- |
|   `users`           |      |
|   `message`                |      |

---



---
### What I Learned




## Author
**My Lu**  
Intern @ Ontash  
Email: myluwork004@gmail.com
LinkedIn : www.linkedin.com/in/my-lu  
Github : https://github.com/MyLu004 
