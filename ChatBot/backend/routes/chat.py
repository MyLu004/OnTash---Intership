# app/routes/chat.py

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import requests
from .. import oauth2
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/chat",
    tags=["Chatbot"]
)

class ChatRequest(BaseModel):
    prompt: str
    model: str = "llama3"

class ChatResponse(BaseModel):
    response: str

@router.post("/", response_model=ChatResponse)
def chat_with_ollama(
    request: ChatRequest,
    token: str = Depends(oauth2.oauth2_scheme)
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
