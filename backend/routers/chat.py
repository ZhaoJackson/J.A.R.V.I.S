from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from ..services.openai_gpt import OpenAIService

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

class ChatResponse(BaseModel):
    response: str

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        openai_service = OpenAIService()
        
        # Add system message
        messages = [
            {
                "role": "system",
                "content": "You are JARVIS, a helpful personal assistant that helps manage various aspects of the user's life including fitness, social media, calendar, books, weather, finance, learning, projects, and entertainment. Be concise and helpful in your responses."
            }
        ]
        
        # Add user messages
        messages.extend([msg.dict() for msg in request.messages])
        
        response = await openai_service.create_chat_completion(messages)
        return ChatResponse(response=response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 