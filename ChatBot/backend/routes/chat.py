
#import neccessary module to run the backend
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import requests
from .. import oauth2, models, schemas
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from ..schemas import ChatCreate
from ..database import get_db
from typing import List

from ..evaluation.deepeval_utils import evaluate_response

#define the router for /chat endpoint
router = APIRouter(
    prefix="/chat",
    tags=["Chatbot"]
)

#set up OAuth2 password bearer for extracting token from Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#define chat response schema


#input format for chatbot request
class ChatRequest(BaseModel):
    prompt: str             # user's prompt or question
    model: str = "llama3"   # default model used for chatbot

#output format for chatbot request
class ChatResponse(BaseModel):
    response: str


# route navigate from login to the chatArea / mainpage for chatbot (Ollama)
@router.post("/", response_model=ChatResponse)
def chat_with_ollama(
    request: ChatRequest,
    token: str = Depends(oauth2_scheme) #token required for accessing this route
):

    try:
        # make a POST request to Ollama server with model and user prompt
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": request.model,
            "prompt": request.prompt,
            "stream": False
        })



        # raise an error if the request to Ollama failed
        response.raise_for_status()

        # parse JSON response from Ollama
        ollama_response = response.json()
        model_reply = ollama_response["response"]

        # evaluate with DeepEval for response relevance
          # safe to import here too
        relevance_score = evaluate_response(
            user_input=request.prompt,
            model_response=model_reply
        )
        print(f"Relevance Score: {relevance_score}")
        #print(f"Using model: {request.model}")

        # return the chatbot response as JSON
        #return {"response": ollama_response["response"]}

        # Return both response and score
        return {"response": model_reply, "relevance_score": relevance_score}
        

    except requests.RequestException as e:
        # return error if the Ollama not reachable
        raise HTTPException(status_code=500, detail="Failed to contact Ollama.")

# Route to save a chat session and its messages to the database
@router.post("/save", status_code=201)
def save_chat(
    chat: ChatCreate,
    db: Session = Depends(get_db),                          # Inject database session
    user: models.User = Depends(oauth2.get_current_user)    # Get current user from token
):
    # Create a new chat record with title and user ID
    db_chat = models.Chat(title=chat.title, user_id=user.id)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat) # refresh to get the chat ID

    # add all the chat message associated with this chat
    for msg in chat.messages:
        db_msg = models.Message(role=msg.role, text=msg.text, chat_id=db_chat.id)
        db.add(db_msg)

    db.commit() #save all the message

    #return the ID for the newly created chat
    return {"chat_id": db_chat.id}


# routes to retrieve all saved chats for the currently logged-in user
@router.get("/chats/", response_model=list[schemas.ChatOut])
def get_chats(
    db: Session = Depends(get_db),
    user: models.User = Depends(oauth2.get_current_user) # get current user
):  
    # query and return all chats that belong to the current user
    return db.query(models.Chat).filter(models.Chat.user_id == user.id).all()
