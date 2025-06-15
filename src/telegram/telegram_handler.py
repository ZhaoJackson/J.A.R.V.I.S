# src/telegram/telegram_handler.py

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from src.commonconst import TELEGRAM_BOT_TOKEN
from src.application.mood_analyzer import analyze_mood_from_text
from src.application.music_player import play_music_by_mood


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Responds to any user message with mood analysis and music playback.
    """
    user_input = update.message.text.strip()
    if not user_input:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="⚠️ Please send some text.")
        return

    mood = analyze_mood_from_text(user_input)
    result = play_music_by_mood(mood)

    if "error" in result:
        reply = f"⚠️ Could not play music: {result['error']}"
    else:
        reply = (
            f"🎧 I detected your mood as *{mood}*.\n"
            f"Now playing music on *{result.get('device', 'an active device')}*."
        )

    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply, parse_mode="Markdown")


def run_telegram_bot():
    """
    Initializes and starts the Telegram bot.
    """
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("🤖 Telegram bot is running and listening for messages...")
    app.run_polling()