# src/modeling/emotion_mappings.py - Emotion Classification Mappings and Configuration

# === Emotion to Playlist Mapping (Data-driven, will be learned by models) ===
EMOTION_PLAYLIST_MAPPING = {
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
    "introspective": "legacy",
    
    # Complex emotions
    "confusion": "mindfulness",
    "gratitude": "surrealism",
    "loneliness": "reflection",
    "overwhelm": "resilience"
}

# === Music Emotion Messages (Psychology-informed) ===
MUSIC_EMOTION_MESSAGES = {
    "positive": {
        "emotions": ["joy", "happy", "excited", "euphoric", "elated", "cheerful", "delighted"],
        "message": "🎶 This upbeat music will amplify your positive energy and support your joyful state!"
    },
    "calm": {
        "emotions": ["calm", "peaceful", "serene", "tranquil", "relaxed"],
        "message": "🎶 This soothing music will deepen your sense of peace and tranquility!"
    },
    "sad": {
        "emotions": ["sad", "melancholy", "sorrowful", "depressed", "lonely"],
        "message": "🎶 This reflective music provides a safe space to process and honor your feelings!"
    },
    "anxious": {
        "emotions": ["anxious", "stressed", "worried", "nervous", "apprehension", "fearful"],
        "message": "🎶 This calming music will help regulate your nervous system and ease tension!"
    },
    "nostalgic": {
        "emotions": ["nostalgic", "reminiscent", "wistful", "sentimental"],
        "message": "🎶 This music will honor your memories and provide comfort in reflection!"
    },
    "complex": {
        "emotions": ["confusion", "gratitude", "loneliness", "overwhelm"],
        "message": "🎶 This music will support you through the complexity of your emotional experience!"
    }
}

def get_playlist_for_emotion(emotion: str) -> str:
    """Get appropriate playlist for emotion (will be replaced by ML model)"""
    return EMOTION_PLAYLIST_MAPPING.get(emotion.lower(), "mindfulness")

def get_music_message_for_emotion(emotion: str, playlist_name: str) -> str:
    """Get appropriate music message for emotion"""
    emotion_lower = emotion.lower()
    
    for category, data in MUSIC_EMOTION_MESSAGES.items():
        if emotion_lower in data["emotions"]:
            return data["message"].format(emotion=emotion)
    
    return f"🎶 This {playlist_name} music will support your {emotion} experience!"
