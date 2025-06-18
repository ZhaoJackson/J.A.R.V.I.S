# src/telegram/telegram_handler.py

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from src.commonconst import TELEGRAM_BOT_TOKEN
from src.interaction.music_mood.music_vs_mood import play_music_by_emotion_text
from src.application.db_manager import log_chat_message


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Responds to user emotion text with mood analysis + Spotify playlist playback.
    """
    user_input = update.message.text.strip()
    chat_id = update.effective_chat.id

    if not user_input:
        await context.bot.send_message(chat_id=chat_id, text="⚠️ Please send a valid emotion or feeling.")
        return

    # Log input to database
    log_chat_message(source="Telegram", message=user_input)

    # Get music recommendation based on emotion
    result = play_music_by_emotion_text(user_input)

    if result["status"] == "success":
        mood = result.get("mood", "unknown")
        device = result.get("device", "your Spotify device")
        playlist = result.get("playlist", "unknown")
        message = result.get("message", "🎵 Music is now playing.")

        if playlist.startswith("Search:"):
            reply = (
                f"🎧 *Mood:* `{mood}`\n"
                f"🔍 *No playlist match.* Used search for: `{mood}`\n"
                f"📱 *Device:* `{device}`\n\n"
                f"{message}"
            )
        else:
            reply = (
                f"🎧 *Mood:* `{mood}`\n"
                f"💿 *Playlist:* `{playlist}`\n"
                f"📱 *Device:* `{device}`\n\n"
                f"{message}"
            )
    else:
        reply = (
            f"❌ *Music playback failed.*\n"
            f"Reason: `{result.get('message', 'Unknown error')}`"
        )

    await context.bot.send_message(chat_id=chat_id, text=reply, parse_mode="Markdown")


def run_telegram_bot():
    """
    Starts the Telegram bot using polling mode.
    """
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("🤖 Telegram bot is running and listening for emotions...")
    app.run_polling()