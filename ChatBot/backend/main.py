from fastapi import FastAPI, Response, status, HTTPException, Depends
from .database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

from . import models

from .database import engine
from .routes import user, auth, chat



models.Base.metadata.create_all(bind=engine) #create table 


app = FastAPI()



# Allow your frontend to talk to your backend
origins = [
    "http://localhost:5173",  # Vite dev server
    "http://127.0.0.1:5173"   # optional, for alternative localhost format
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] to allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user.router)
app.include_router(auth.router)
app.include_router(chat.router) 




@app.get("/") 
def root():

    #the data get send back to the client
    return {"message": "Hello World kinoko from FastAPI! :3"}