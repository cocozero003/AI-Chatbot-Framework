import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from .engine import ChatbotEngine

load_dotenv()
logging.basicConfig(level=logging.INFO)
app = FastAPI(title="AI Chatbot w/ Human-in-Loop", version="0.1.0")
bot = ChatbotEngine()

class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        reply = bot.process(req.user_id, req.message)
        return ChatResponse(reply=reply)
    except Exception as e:
        logging.error("Processing error: %s", e)
        raise HTTPException(status_code=500, detail="Internal server error")
