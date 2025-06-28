# src/telegram/telegram_handler.py

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from src.commonconst import TELEGRAM_BOT_TOKEN_MUSIC
from src.interaction.music_mood.music_vs_mood import (
    play_music_by_emotion_text,
    record_music_feedback
)
from src.application.db_manager import log_chat_message

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()
    chat_id = update.effective_chat.id

    if not user_input:
        await context.bot.send_message(chat_id=chat_id, text="⚠️ Please send a valid emotion or feeling.")
        return

    # Check if user replied with feedback ("yes"/"no")
    if user_input.lower() in ["yes", "no"] and "feedback_context" in context.user_data:
        fb = context.user_data["feedback_context"]
        feedback_result = record_music_feedback(
            user_input=fb["user_input"],
            detected_mood=fb["detected_mood"],
            playlist=fb["playlist"],
            song_name=fb["song_name"],
            user_feedback=user_input.lower(),
            source="telegram"
        )
        await context.bot.send_message(chat_id=chat_id, text=f"🙏 Thanks for your feedback! {feedback_result}")
        context.user_data.pop("feedback_context")
        return

    # Otherwise: Treat input as emotion
    log_chat_message(source="Telegram", message=user_input)

    result = play_music_by_emotion_text(user_input, source="telegram")

    if result["status"] == "success":
        mood = result.get("mood", "unknown")
        playlist = result.get("playlist", "unknown")
        device = result.get("device", "your Spotify device")
        message = result.get("message", "🎵 Music is now playing.")
        feedback_prompt = result.get("feedback_prompt")

        reply = (
            f"🎧 *Mood:* `{mood}`\n"
            f"💿 *Playlist:* `{playlist}`\n"
            f"📱 *Device:* `{device}`\n\n"
            f"{message}"
        )
        if feedback_prompt:
            reply += f"\n\n{feedback_prompt}"

        # Store for next feedback input
        context.user_data["feedback_context"] = {
            "user_input": user_input,
            "detected_mood": mood,
            "playlist": playlist,
            "song_name": "random_song",
        }

    else:
        reply = (
            f"❌ *Music playback failed.*\n"
            f"Reason: `{result.get('message', 'Unknown error')}`"
        )

    await context.bot.send_message(chat_id=chat_id, text=reply, parse_mode="Markdown")


def run_telegram_bot():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN_MUSIC).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("🤖 Telegram bot is running and listening for emotions...")
    app.run_polling()