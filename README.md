# J.A.R.V.I.S. – Just A Rather Very Intelligent System 🎧🧠

J.A.R.V.I.S. is a modular FastAPI-based personal assistant that detects mood from your diary entries and plays corresponding Spotify playlists. It integrates with:

- ✅ **Ollama LLM** for natural language mood analysis  
- ✅ **Spotify API** for mood-driven music playback  
- ✅ **SQLite** logging system for diary, mood, and music history  

---

## 📦 Project Structure

```
J.A.R.V.I.S/
│
├── main.py                       # FastAPI main app
├── requirements.txt              # Python dependencies
├── commonconst.py                # Global variables and paths
│
├── router/
│   ├── log_routes.py             # Logs diary entries and moods
│   ├── mood_routes.py            # Detects mood and plays music
│   ├── music_routes.py           # Manually play music by mood
│   └── interaction/
│       └── music_vs_mood.py      # Helper for LLM + Spotify logic
│
├── db/
│   └── jarvis_logs.db            # SQLite database (auto-generated)
└── .env                          # Secret keys (not committed)
```

---

## ⚙️ Setup Instructions

### 1. Create `.env` File

```
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
SPOTIPY_REDIRECT_URI=your url
OLLAMA_URL=your url
OLLAMA_MODEL=your model
```

> ⚠️ You need a Spotify **Premium** account and active device for playback.

---

### 2. Install Requirements

```bash
conda create -n ollama_env python=3.9
conda activate ollama_env
pip install -r requirements.txt
```

---

### 3. Run the Server

```bash
uvicorn main:app --reload --port 8001
```

FastAPI app will be available at: [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)

---

## 🧪 API Endpoints

### 1. Log a Diary Entry and Auto-Play Music

```bash
curl -X POST http://127.0.0.1:8001/api/analyze-mood-and-play \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"diary_entry": "I feel burned out but tried to stay calm by walking in the park."}'
```

**Response:**

```json
{
  "diary_entry": "...",
  "mood": "calm",
  "music": {
    "status": "playing",
    "device": "YourDevice",
    "mood": "calm"
  }
}
```

---

### 2. Play Music Manually by Mood

```bash
curl -X GET "http://127.0.0.1:8001/api/music/play?mood=happy"
```

---

### 3. Retrieve All Logs

```bash
curl -X GET http://127.0.0.1:8001/api/logs
```

---

## 🎶 Supported Moods

```
happy, sad, calm, angry, focused,
joyful, frustrated, peaceful, excited, heartbroken, studying, relaxed, neutral, unsure
```

---

## ✅ Features

- 🔁 Automatically stores diary and mood logs  
- 🤖 Uses Ollama’s LLM to infer your emotional state  
- 🎧 Starts playback based on mood using Spotify API  
- 🔍 Simple curl or REST interaction (frontend optional)  

---

## 🛡️ Security

- All credentials are stored in `.env`  
- API runs locally by default (safe for personal use)  

---

## 💡 Future Ideas

- Voice input and playback with ElevenLabs or Coqui  
- Daily summary of moods + music logs  
- Integration with n8n or Telegram  

---

## 🤖 Author

**Jackson Zhao** · Data Scientist & AI Builder · [GitHub](https://github.com/)

---

> _“I am J.A.R.V.I.S. — your mood-aware, music-triggering AI sidekick.”_