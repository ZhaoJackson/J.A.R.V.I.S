# src/application/core_engine.py - Streamlined Core JARVIS Engine

from typing import Dict, List
from collections import defaultdict
import requests
from src.modeling.simple_emotion_model import simple_emotion_classifier
from src.modeling.intelligent_selector import intelligent_selector
from src.modeling.self_learning_engine import self_learning_engine
from src.vector_space.philosophy_rag import philosophy_rag
from src.application.psychology_prompts import psychology_prompts
from src.application.db_manager import log_emotion_session
from src.application.music_engine import play_music_for_emotion
from src.commonconst import OLLAMA_URL, OLLAMA_MODEL, OLLAMA_TIMEOUT

class JARVISCoreEngine:
    """Streamlined core engine with self-learning capabilities"""
    
    def __init__(self):
        self.emotion_classifier = simple_emotion_classifier
        self.intelligent_selector = intelligent_selector
        self.learning_engine = self_learning_engine
        self.philosophy_rag = philosophy_rag
        self.psychology_prompts = psychology_prompts
        
    def initialize_systems(self):
        """Initialize all AI systems"""
        print("🔨 Initializing emotion classification...")
        test_result = self.emotion_classifier.classify_emotion_hybrid("I feel happy")
        print(f"✅ Emotion system ready: {test_result['primary_emotion']}")
        
        print("📚 Building philosophy knowledge base...")
        self.philosophy_rag.build_embeddings()
        
        print("📈 Loading learning patterns...")
        self.learning_engine.learn_from_interactions()
        
        print("✅ All systems initialized!")
    
    def process_emotion(self, text: str, user_id: str = "default") -> Dict:
        """Process emotional input with self-learning"""
        
        # Step 1: Classify emotion using hybrid approach
        emotion_result = self.emotion_classifier.classify_emotion_hybrid(text)
        primary_emotion = emotion_result['primary_emotion']
        
        # Step 2: Get learned preferences for this emotion
        learned_prefs = self.learning_engine.get_learned_preferences(primary_emotion)
        
        # Step 3: Select books using AI + learned preferences
        complexity_analysis = self.intelligent_selector.analyze_emotion_complexity(text, primary_emotion)
        
        if learned_prefs['learning_confidence'] > 0.3:
            # Use learned preferences
            preferred_books = [book for book, score in learned_prefs['preferred_books'][:2]]
            book_selection_method = "learned_preferences"
        else:
            # Use AI selector
            selected_books = self.intelligent_selector.select_relevant_books(
                primary_emotion, text, top_k=complexity_analysis['recommended_book_count']
            )
            preferred_books = [book['book'] for book in selected_books]
            book_selection_method = "ai_selection"
        
        # Step 4: Search philosophy content across selected books
        philosophy_sources = []
        for book in preferred_books:
            book_query = f"{text} {primary_emotion} {book}"
            book_sources = self.philosophy_rag.search_relevant_content(book_query, top_k=3)
            philosophy_sources.extend(book_sources)
        
        # Step 5: Generate therapeutic response
        therapeutic_response = self.generate_therapeutic_response(
            text, primary_emotion, philosophy_sources
        )
        
        # Step 6: Select music using learned preferences
        if learned_prefs['preferred_playlists']:
            playlist_name = learned_prefs['preferred_playlists'][0][0]
            music_selection_method = "learned_preferences"
        else:
            playlist_result = self.intelligent_selector.select_optimal_playlist(primary_emotion, text)
            playlist_name = playlist_result['playlist']
            music_selection_method = "ai_selection"
        
        # Step 7: Play music
        music_result = play_music_for_emotion(text, primary_emotion)
        
        # Step 8: Log interaction for future learning
        log_emotion_session(
            user_input=text,
            detected_emotion=primary_emotion,
            selected_book=preferred_books[0] if preferred_books else 'none',
            music_playlist=playlist_name,
            music_status=music_result.get('status', 'unknown'),
            session_id=user_id
        )
        
        # Step 9: Update learning patterns (reinforcement)
        self.learning_engine.update_learning_from_new_interaction(
            text, primary_emotion, preferred_books[0] if preferred_books else 'none', playlist_name
        )
        
        return {
            "status": "success",
            "emotion": primary_emotion,
            "confidence": emotion_result['confidence'],
            "philosophy": {
                "response": therapeutic_response,
                "books_referenced": preferred_books,
                "sources_count": len(philosophy_sources),
                "selection_method": book_selection_method
            },
            "music": {
                "playlist": playlist_name,
                "device": music_result.get('device'),
                "message": music_result.get('message'),
                "selection_method": music_selection_method
            },
            "learning": {
                "learning_confidence": learned_prefs['learning_confidence'],
                "complexity_score": complexity_analysis['complexity_score'],
                "method_used": emotion_result.get('method', 'hybrid')
            }
        }
    
    def generate_therapeutic_response(self, text: str, emotion: str, sources: List[Dict]) -> str:
        """Generate therapeutic response using philosophy sources"""
        
        if not sources:
            return f"I understand you're feeling {emotion}. While I don't have specific philosophical guidance for your exact situation, your emotions are valid and seeking support shows wisdom."
        
        # Group sources by book for attribution
        sources_by_book = defaultdict(list)
        for source in sources:
            sources_by_book[source['book']].append(source)
        
        # Create prompt with multi-book sources
        formatted_sources = ""
        for book, book_sources in sources_by_book.items():
            formatted_sources += f"\n=== {book.upper()} ===\n"
            for i, source in enumerate(book_sources[:2], 1):  # Top 2 per book
                formatted_sources += f"{i}. \"{source['source']}\" - {source['translation']}\n"
        
        books_used = list(sources_by_book.keys())
        
        prompt = f"""You are a wise counselor integrating ancient philosophy with modern understanding.

A person feeling "{emotion}" shared: "{text}"

Relevant wisdom from multiple traditions:
{formatted_sources}

Create a compassionate response that:
1. Acknowledges their {emotion} with empathy
2. Integrates wisdom from the sources above (cite which tradition each comes from)
3. Provides practical guidance
4. Shows how different philosophical traditions complement each other
5. Keeps it concise but meaningful

Books referenced: {', '.join(books_used)}

Response:"""

        try:
            response = requests.post(
                f"{OLLAMA_URL}/api/generate",
                json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
                timeout=OLLAMA_TIMEOUT
            )
            
            if response.ok:
                return response.json().get("response", "").strip()
            
        except Exception as e:
            print(f"❌ Response generation failed: {e}")
        
        return f"I understand you're experiencing {emotion}. The wisdom traditions offer guidance, though I'm having difficulty accessing specific quotes right now. Your feelings are valid and seeking wisdom shows strength."

# Global instance
jarvis_core = JARVISCoreEngine()