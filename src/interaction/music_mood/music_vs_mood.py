# src/interaction/music_mood/music_vs_mood.py

from sentence_transformers import util
from src.application.mood_analyzer import analyze_emotion
from src.application.music_player import play_playlist
from src.commonconst import SPOTIFY_PLAYLISTS, EMBEDDING_MODEL

def match_emotion_to_playlist(emotion: str) -> str:
    """Match emotion to best playlist using improved emotion mapping"""
    emotion_lower = emotion.lower()
    
    # Define explicit emotion-to-playlist mappings for better accuracy
    emotion_mappings = {
        # Happy/Positive emotions
        "joy": "surrealism",
        "happy": "surrealism", 
        "excited": "surrealism",
        "euphoric": "surrealism",
        "elated": "surrealism",
        "cheerful": "surrealism",
        "delighted": "surrealism",
        
        # Calm/Peaceful emotions  
        "calm": "mindfulness",
        "peaceful": "mindfulness",
        "serene": "mindfulness",
        "tranquil": "mindfulness",
        "relaxed": "mindfulness",
        
        # Sad/Melancholic emotions
        "sad": "reflection",
        "melancholy": "reflection", 
        "sorrowful": "reflection",
        "depressed": "reflection",
        "lonely": "reflection",
        
        # Anxious/Stressed emotions
        "anxious": "resilience",
        "stressed": "resilience",
        "worried": "resilience", 
        "nervous": "resilience",
        "apprehension": "resilience",
        "fearful": "resilience",
        
        # Nostalgic/Reflective emotions
        "nostalgic": "memory",
        "reminiscent": "memory",
        "wistful": "memory",
        "sentimental": "memory",
        
        # Deep/Profound emotions
        "contemplative": "legacy",
        "philosophical": "legacy",
        "profound": "legacy",
        "introspective": "legacy"
    }
    
    # Check for direct mapping first
    if emotion_lower in emotion_mappings:
        return emotion_mappings[emotion_lower]
    
    # Fall back to semantic similarity if no direct match
    playlist_names = list(SPOTIFY_PLAYLISTS.keys())
    emotion_embedding = EMBEDDING_MODEL.encode(emotion, convert_to_tensor=True)
    playlist_embeddings = EMBEDDING_MODEL.encode(playlist_names, convert_to_tensor=True)
    
    scores = util.cos_sim(emotion_embedding, playlist_embeddings)[0]
    best_index = scores.argmax().item()
    return playlist_names[best_index]

def get_emotion_music_message(emotion: str, playlist_name: str) -> str:
    """Generate context-appropriate music message based on emotion"""
    from src.commonconst import BOT_NAME
    
    emotion_lower = emotion.lower()
    
    # Define emotion categories and their messages
    emotion_messages = {
        "positive": ["joy", "happy", "excited", "euphoric", "elated", "cheerful", "delighted"],
        "calm": ["calm", "peaceful", "serene", "tranquil", "relaxed"],
        "sad": ["sad", "melancholy", "sorrowful", "depressed", "lonely"],
        "anxious": ["anxious", "stressed", "worried", "nervous", "apprehension", "fearful"],
        "nostalgic": ["nostalgic", "reminiscent", "wistful", "sentimental"]
    }
    
    messages = {
        "positive": f"🎶 Perfect! This upbeat music will match your {emotion} energy!",
        "calm": f"🎶 This soothing music will enhance your {emotion} state!",
        "sad": f"🎶 This reflective music will help you process your {emotion} feelings!",
        "anxious": f"🎶 This calming music should help ease your {emotion} feelings!",
        "nostalgic": f"🎶 This music will complement your {emotion} mood perfectly!"
    }
    
    for category, emotions in emotion_messages.items():
        if emotion_lower in emotions:
            return messages[category]
    
    return f"🎶 This {playlist_name} music suits your {emotion} mood!"

def play_music_for_emotion(text: str) -> dict:
    """Main function: analyze emotion and play matching music"""
    emotion = analyze_emotion(text)
    playlist_name = match_emotion_to_playlist(emotion)
    playlist_id = SPOTIFY_PLAYLISTS.get(playlist_name)
    
    if not playlist_id:
        return {"status": "error", "message": "❌ No playlist found for this emotion"}
    
    # Try to play the playlist
    result = play_playlist(playlist_id)
    
    if result.get("status") == "success":
        # Real Spotify playback successful
        music_message = get_emotion_music_message(emotion, playlist_name)
        return {
            "status": "success",
            "emotion": emotion,
            "playlist": playlist_name,
            "device": result.get("device"),
            "message": f"🎵 {playlist_name.title()} playlist now playing on {result.get('device')}\n{music_message}"
        }
    else:
        # Spotify error - return the error message
        return {
            "status": "error",
            "emotion": emotion,
            "playlist": playlist_name,
            "device": None,
            "message": result.get("message", "❌ Music playback failed")
        }

