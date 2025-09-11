# J.A.R.V.I.S. – Simplified Emotional Support System 🧠🎵

A streamlined AI assistant that provides emotional support through:
- 🧠 **Emotion Analysis** using Ollama LLM
- 📚 **Philosophical Wisdom** from ancient texts and psychology books  
- 🎵 **Mood-based Music** via Spotify integration
- 💬 **Telegram Bot** for easy interaction

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Create conda environment
conda create -n jarvis_env python=3.9
conda activate jarvis_env

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create `.env` file:
```bash
# Ollama Configuration
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3

# Telegram Bot
TELEGRAM_BOT_TOKEN_PHILOSOPHY=your_telegram_bot_token

# Spotify (Optional - will use simulation mode if not configured)
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
SPOTIPY_REDIRECT_URI=http://localhost:8080/callback
```

### 3. Run JARVIS
```bash
python bot_launcher.py
```

## 📁 Project Structure

```
J.A.R.V.I.S/
├── main.py                   # Core JARVIS logic
├── bot_launcher.py           # Bot launcher
├── analyze_emotions.py       # Data analysis & visualization
├── src/
│   ├── telegram_bot.py      # Telegram integration
│   ├── commonconst.py       # All configuration (no hardcoding)
│   ├── application/
│   │   ├── mood_analyzer.py    # Emotion detection
│   │   ├── philosopher.py      # Philosophy matching
│   │   ├── music_player.py     # Real Spotify integration
│   │   └── db_manager.py       # Comprehensive logging
│   ├── interaction/music_mood/
│   │   └── music_vs_mood.py    # Music-emotion matching
│   └── book/                   # Philosophy books (JSON)
│       ├── analects.json
│       ├── iching.json
│       ├── mencius.json
│       ├── positive_psy.json
│       ├── social_psy.json
│       └── tao_te_ching.json
└── db/
    ├── emotion_logs.db         # Comprehensive emotion logging
    ├── emotion_history.csv     # Exportable data
    └── emotion_analysis.png    # Visualization charts
```

## 🔄 How It Works

1. **User Input**: Send emotional message via Telegram
2. **Emotion Analysis**: Ollama analyzes the emotion
3. **Philosophy Matching**: AI selects most relevant philosophy book
4. **Quote Extraction**: Finds relevant quotes using semantic similarity
5. **Music Selection**: Matches emotion to Spotify playlist
6. **Response**: Combines philosophical wisdom with music recommendation

## 🎵 Spotify Integration

- **With Credentials**: Plays actual playlists on your devices
- **Without Credentials**: Simulation mode with realistic responses
- **Auto-Detection**: System automatically detects availability

## 📚 Philosophy Books Included

- **Analects** - Confucian wisdom
- **I Ching** - Ancient Chinese divination
- **Mencius** - Confucian philosophy
- **Tao Te Ching** - Taoist philosophy
- **Positive Psychology** - Modern psychological concepts
- **Social Psychology** - Social behavior insights

## 💡 Example Usage

**User**: "I feel stressed about my upcoming presentation"

**JARVIS Response**:
- 🧠 **Emotion**: Anxious
- 📚 **Wisdom from Analects**: *[Relevant quote about preparation and confidence]*
- 🎵 **Music**: Resilience playlist now playing on iPhone

## 📊 Data Analysis Features

**Commands Available:**
- `/status` - View system status and emotion statistics
- `/export` - Export emotion history to CSV
- `python analyze_emotions.py` - Generate visualization charts

**What Gets Logged:**
- Timestamp of each interaction
- Your emotional input text
- Detected emotion
- Selected philosophy book
- Philosopher's response
- Music playlist played
- Spotify device used

## 🛠️ Technical Features

- **Semantic Matching**: Uses sentence transformers for intelligent book/music selection
- **Relative Paths**: All paths are relative for easy deployment
- **Minimal Dependencies**: Streamlined codebase with only essential components
- **Error Resilience**: Graceful fallbacks when services are unavailable
- **Single Bot**: Unified Telegram bot handling all functionality

## 🎯 Core Philosophy

This version focuses on:
- **Simplicity**: Minimal code, maximum impact
- **Reliability**: Robust error handling and fallbacks  
- **Intelligence**: Semantic matching for better responses
- **Accessibility**: Easy setup and deployment