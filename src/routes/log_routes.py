# src/routes/log_routes.py

from fastapi import APIRouter
from pydantic import BaseModel
from src.application.db_manager import log_diary_entry, log_chat_message

router = APIRouter()

class DiaryLogInput(BaseModel):
    content: str

class ChatLogInput(BaseModel):
    source: str
    message: str

@router.post("/log/diary")
async def log_diary(entry: DiaryLogInput):
    """
    Log a personal diary entry (text input from the user).
    """
    log_diary_entry(entry.content)
    return {"status": "✅ Diary entry saved successfully."}

@router.post("/log/chat")
async def log_chat(chat: ChatLogInput):
    """
    Log any chat message, such as those from Telegram or voice assistant.
    """
    log_chat_message(chat.source, chat.message)
    return {"status": f"✅ Chat message from '{chat.source}' logged."}