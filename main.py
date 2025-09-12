# main.py - JARVIS Streamlined Self-Learning System

from src.application.core_engine import jarvis_core

def initialize_advanced_systems():
    """Initialize the self-learning AI systems"""
    jarvis_core.initialize_systems()

def process_emotion_request(text: str, user_id: str = "default") -> dict:
    """
    Main JARVIS function with self-learning capabilities:
    1. Emotion classification with learned preferences
    2. Multi-book RAG responses with source attribution
    3. Music selection based on learned effectiveness
    4. Continuous learning from interactions
    """
    return jarvis_core.process_emotion(text, user_id)

if __name__ == "__main__":
    # Initialize systems
    initialize_advanced_systems()
    
    # Test self-learning system
    result = process_emotion_request("I feel confused but hopeful about my future", "test_user")
    print(f"✅ Self-learning test successful!")
    print(f"Emotion: {result['emotion']} (confidence: {result['confidence']:.2f})")
    print(f"Books: {result['philosophy']['books_referenced']} ({result['philosophy']['selection_method']})")
    print(f"Music: {result['music']['playlist']} ({result['music']['selection_method']})")
    print(f"Learning confidence: {result['learning']['learning_confidence']:.2f}")
    print(f"Response preview: {result['philosophy']['response'][:100]}...")