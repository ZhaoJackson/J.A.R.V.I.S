# src/routes/log_routes.py

from fastapi import APIRouter
from pydantic import BaseModel
from src.application.db_manager import log_diary_entry, log_chat_message

router = APIRouter()

# === Request Models ===
class DiaryLogInput(BaseModel):
    content: str

class ChatLogInput(BaseModel):
    source: str
    message: str

# === Routes ===
@router.post("/log/diary")
async def log_diary(entry: DiaryLogInput) -> dict:
    """
    Log a diary entry with timestamp.
    Example usage: {"content": "Today I felt excited and motivated."}
    """
    log_diary_entry(entry.content)
    return {"status": "✅ Diary entry saved successfully."}

@router.post("/log/chat")
async def log_chat(chat: ChatLogInput) -> dict:
    """
    Log a chat message from any source (e.g., Telegram, Voice Assistant).
    Example usage: {"source": "Telegram", "message": "Play me a happy song."}
    """
    log_chat_message(chat.source, chat.message)
    return {"status": f"✅ Chat message from '{chat.source}' logged."}