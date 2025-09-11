# main.py - JARVIS Main System

from src.application.mood_analyzer import analyze_emotion
from src.application.philosopher import provide_emotional_support
from src.interaction.music_mood.music_vs_mood import play_music_for_emotion
from src.application.db_manager import log_emotion_session

def process_emotion_request(text: str, user_id: str = "default") -> dict:
    """
    Main JARVIS function that processes emotional input and provides:
    1. Emotion analysis
    2. Philosophical support  
    3. Music recommendation
    4. Complete logging
    """
    # Analyze emotion
    emotion = analyze_emotion(text)
    
    # Get philosophical support
    philosophy_result = provide_emotional_support(text, emotion)
    
    # Play appropriate music
    music_result = play_music_for_emotion(text)
    
    # Log the complete session
    log_emotion_session(
        user_input=text,
        detected_emotion=emotion,
        selected_book=philosophy_result.get("book_used"),
        philosopher_response=philosophy_result.get("response"),
        music_playlist=music_result.get("playlist"),
        music_device=music_result.get("device"),
        music_status=music_result.get("status"),
        session_id=user_id
    )
    
    # Return combined results
    return {
        "status": "success",
        "emotion": emotion,
        "philosophy": {
            "book": philosophy_result.get("book_used"),
            "response": philosophy_result.get("response")
        },
        "music": {
            "playlist": music_result.get("playlist"),
            "device": music_result.get("device"),
            "message": music_result.get("message")
        }
    }

if __name__ == "__main__":
    # Simple test
    result = process_emotion_request("I feel happy today")
    print(f"Emotion: {result['emotion']}")
    print(f"Book: {result['philosophy']['book']}")
    print(f"Music: {result['music']['playlist']}")
