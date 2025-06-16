# src/telegram/telegram_handler.py

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from src.commonconst import TELEGRAM_BOT_TOKEN
from src.interaction.music_mood.music_vs_mood import play_music_by_emotional_text

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Responds to user text with mood analysis and Spotify playlist playback.
    """
    user_input = update.message.text.strip()
    chat_id = update.effective_chat.id

    if not user_input:
        await context.bot.send_message(chat_id=chat_id, text="⚠️ Please send some text.")
        return

    result = play_music_by_emotional_text(user_input)

    # Compose response message
    if result["status"] == "playing":
        mood = result.get("mood", "unknown")
        device = result.get("device", "your Spotify device")
        reply = f"🎧 Mood detected: *{mood}*.\nNow playing music on *{device}*."
    else:
        reply = f"⚠️ Could not play music.\nReason: {result.get('message')}"

    await context.bot.send_message(chat_id=chat_id, text=reply, parse_mode="Markdown")

def run_telegram_bot():
    """
    Starts the Telegram bot using polling.
    """
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("🤖 Telegram bot is running and listening for messages...")
    app.run_polling()