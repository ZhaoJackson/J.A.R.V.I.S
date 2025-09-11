# src/telegram_bot.py - JARVIS Telegram Bot

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from src.application.db_manager import export_emotions_to_csv, get_emotion_statistics, log_emotion_session
from src.application.music_player import is_spotify_configured
from src.application.mood_analyzer import analyze_emotion
from src.application.philosopher import provide_emotional_support
from src.interaction.music_mood.music_vs_mood import play_music_for_emotion
from src.commonconst import (
    TELEGRAM_BOT_TOKEN_PHILOSOPHY, 
    WELCOME_MESSAGE, 
    ERROR_MESSAGE_TEMPLATE,
    BOT_NAME
)

def process_emotion_request_safe(text: str, user_id: str = "default") -> dict:
    """Safe version of emotion processing that doesn't block on Spotify"""
    try:
        # Analyze emotion
        emotion = analyze_emotion(text)
        
        # Get philosophical support
        philosophy_result = provide_emotional_support(text, emotion)
        
        # Try music but don't block on Spotify errors
        try:
            music_result = play_music_for_emotion(text)
        except Exception as e:
            music_result = {
                "status": "error",
                "playlist": "none",
                "device": None,
                "message": f"❌ Music unavailable: {str(e)}"
            }
        
        # Log the session
        log_emotion_session(
            user_input=text,
            detected_emotion=emotion,
            selected_book=philosophy_result.get("book_used"),
            philosopher_response=philosophy_result.get("response"),
            music_playlist=music_result.get("playlist"),
            music_device=music_result.get("device"),
            music_status=music_result.get("status"),
            session_id=user_id
        )
        
        return {
            "status": "success",
            "emotion": emotion,
            "philosophy": {
                "book": philosophy_result.get("book_used"),
                "response": philosophy_result.get("response")
            },
            "music": {
                "playlist": music_result.get("playlist"),
                "device": music_result.get("device"),
                "message": music_result.get("message")
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "emotion": "unknown",
            "philosophy": {"book": "none", "response": f"Philosophy error: {str(e)}"},
            "music": {"playlist": "none", "device": None, "message": f"Music error: {str(e)}"}
        }

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    await update.message.reply_text(WELCOME_MESSAGE)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command"""
    spotify_status = "✅ Configured" if is_spotify_configured() else "❌ Not configured"
    stats = get_emotion_statistics()
    
    status_msg = f"""🔧 {BOT_NAME} System Status:

📱 Spotify: {spotify_status}
📊 Total Sessions: {stats['total_sessions']}
😊 Top Emotion: {stats['top_emotions'][0][0] if stats['top_emotions'] else 'None'}
📚 Favorite Book: {stats['top_books'][0][0] if stats['top_books'] else 'None'}

Use /export to download your emotion history as CSV."""
    await update.message.reply_text(status_msg)

async def export_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /export command"""
    try:
        csv_path = export_emotions_to_csv()
        await update.message.reply_text(f"📊 Emotion history exported to: {csv_path.name}")
    except Exception as e:
        await update.message.reply_text(f"❌ Export failed: {str(e)}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all text messages"""
    user_input = update.message.text
    user_id = str(update.effective_user.id)
    
    try:
        # Show typing indicator
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        # Process the emotional request with safe error handling
        result = process_emotion_request_safe(user_input, user_id)
        
        # Format response (plain text to avoid Markdown parsing errors)
        response = f"""🧠 Emotion Detected: {result['emotion']}

📚 Wisdom from {result['philosophy']['book']}:
{result['philosophy']['response']}

🎵 Music: {result['music']['message']}"""
        
        await update.message.reply_text(response)
        
    except Exception as e:
        print(f"❌ Error processing message: {e}")
        error_response = ERROR_MESSAGE_TEMPLATE.format(error=str(e))
        await update.message.reply_text(error_response)

def run_telegram_bot():
    """Run the Telegram bot"""
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN_PHILOSOPHY).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("export", export_data))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print(f"🤖 {BOT_NAME} Telegram bot is running...")
    app.run_polling()
