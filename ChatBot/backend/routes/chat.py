# app/routes/chat.py

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import requests
from .. import oauth2, models, schemas
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from ..schemas import ChatCreate


from ..database import get_db
from typing import List


router = APIRouter(
    prefix="/chat",
    tags=["Chatbot"]
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class ChatRequest(BaseModel):
    prompt: str
    model: str = "llama3"

class ChatResponse(BaseModel):
    response: str

@router.post("/", response_model=ChatResponse)
def chat_with_ollama(
    request: ChatRequest,
    token: str = Depends(oauth2_scheme)
):
    # TODO : fix the token authorization later
    # Verify token
    #_ = oauth2.verify_access_token(token, HTTPException(status_code=401, detail="Invalid token"))

    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": request.model,
            "prompt": request.prompt,
            "stream": False
        })

        response.raise_for_status()
        ollama_response = response.json()
        
        print(f"Using model: {request.model}")

        return {"response": ollama_response["response"]}

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail="Failed to contact Ollama.")

   
@router.post("/save", status_code=201)
def save_chat(
    chat: ChatCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(oauth2.get_current_user)
):
    db_chat = models.Chat(title=chat.title, user_id=user.id)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)

    for msg in chat.messages:
        db_msg = models.Message(role=msg.role, text=msg.text, chat_id=db_chat.id)
        db.add(db_msg)

    db.commit()
    return {"chat_id": db_chat.id}

# @router.get("/chats/")
# def get_chats(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
#     chats = db.query(models.Chat).filter(models.Chat.user_id == user_id).all()
#     return chats

@router.get("/chats/", response_model=list[schemas.ChatOut])
def get_chats(
    db: Session = Depends(get_db),
    user: models.User = Depends(oauth2.get_current_user)
):
    return db.query(models.Chat).filter(models.Chat.user_id == user.id).all()
