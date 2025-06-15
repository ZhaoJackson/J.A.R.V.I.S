# src/routes/log_routes.py
from fastapi import APIRouter, Body
from src.application.db_manager import log_diary_entry, log_chat_message

router = APIRouter()

@router.post("/log/diary")
async def log_diary(content: str = Body(..., embed=True)):
    """
    Log a personal diary entry (text input from the user).
    """
    log_diary_entry(content)
    return {"status": "✅ Diary entry saved successfully."}

@router.post("/log/chat")
async def log_chat(source: str = Body(...), message: str = Body(...)):
    """
    Log any chat message, such as those from Telegram or voice assistant.
    """
    log_chat_message(source, message)
    return {"status": f"✅ Chat message from '{source}' logged."}