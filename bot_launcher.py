# bot_launcher.py - JARVIS Bot Launcher

import signal
import sys
from src.telegram_bot import run_telegram_bot
from src.commonconst import BOT_NAME, BOT_VERSION

def signal_handler(sig, frame):
    """Handle shutdown signals gracefully"""
    print(f"\n🛑 Shutting down {BOT_NAME} bot...")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print(f"🚀 Launching {BOT_NAME} v{BOT_VERSION} Telegram Bot...")
    print("=" * 50)
    print("🎵 Music System: Real Spotify integration")
    print("📚 Philosophy System: Semantic book matching")
    print("🧠 Emotion Analysis: Powered by Ollama")
    print("📊 Database: Comprehensive emotion logging")
    print("=" * 50)
    print("Press Ctrl+C to stop the bot")
    
    try:
        run_telegram_bot()
    except Exception as e:
        print(f"❌ Bot error: {e}")
    finally:
        print(f"✅ {BOT_NAME} bot stopped.")