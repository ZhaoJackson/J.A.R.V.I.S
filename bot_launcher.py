# bot_launcher.py - JARVIS Bot Launcher with Advanced ML Pipeline

import signal
import sys
from src.telegram_bot import run_telegram_bot
from src.commonconst import BOT_NAME, BOT_VERSION
from main import initialize_advanced_systems

def signal_handler(sig, frame):
    """Handle shutdown signals gracefully"""
    print(f"\n🛑 Shutting down {BOT_NAME} bot...")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print(f"🚀 Launching {BOT_NAME} v{BOT_VERSION} Advanced AI Therapist...")
    print("=" * 60)
    print("🧠 Emotion Analysis: Advanced ML Pipeline")
    print("📚 Philosophy System: RAG Framework with Vector Database")
    print("🎵 Music System: Real Spotify Integration")
    print("📊 Database: Comprehensive Emotion Logging")
    print("🔬 Psychology: Clinical-grade Analysis")
    print("=" * 60)
    
    # Initialize advanced systems
    print("🔧 Initializing advanced AI systems...")
    initialize_advanced_systems()
    
    print("Press Ctrl+C to stop the bot")
    
    try:
        run_telegram_bot()
    except Exception as e:
        print(f"❌ Bot error: {e}")
    finally:
        print(f"✅ {BOT_NAME} bot stopped.")