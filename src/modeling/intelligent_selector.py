# src/modeling/intelligent_selector.py - Model-driven Selection for Playlists and Books

import numpy as np
from typing import List, Dict, Tuple
from sentence_transformers import util
from src.commonconst import SPOTIFY_PLAYLISTS, AVAILABLE_BOOKS, EMBEDDING_MODEL

class IntelligentSelector:
    """Model-driven selection system for playlists and philosophy books"""
    
    def __init__(self):
        self.embedding_model = EMBEDDING_MODEL
        self.playlist_descriptions = {
            "surrealism": "upbeat energetic happy joyful celebratory positive vibrant",
            "legacy": "deep contemplative profound meaningful introspective thoughtful",
            "reflection": "sad melancholic sorrowful reflective processing healing",
            "memory": "nostalgic reminiscent sentimental past memories longing",
            "mindfulness": "calm peaceful serene tranquil meditative relaxing",
            "resilience": "strong overcoming challenges stress relief empowering"
        }
        
        self.book_descriptions = {
            "analects": "practical wisdom social harmony relationships ethics moral guidance",
            "iching": "change transformation cycles balance cosmic wisdom divination",
            "mencius": "human nature goodness moral cultivation benevolence righteousness",
            "tao_te_ching": "natural flow simplicity wu wei balance harmony effortless action",
            "positive_psy": "happiness wellbeing strengths resilience optimism flourishing",
            "social_psy": "social behavior relationships groups influence psychology research"
        }
    
    def select_optimal_playlist(self, emotion: str, emotional_context: str = "") -> str:
        """Use semantic similarity to select the most appropriate playlist"""
        # Combine emotion with context for better matching
        query = f"{emotion} {emotional_context}".strip()
        
        # Create embeddings
        query_embedding = self.embedding_model.encode([query])
        
        # Get playlist embeddings
        playlist_names = list(self.playlist_descriptions.keys())
        playlist_descriptions = [self.playlist_descriptions[name] for name in playlist_names]
        playlist_embeddings = self.embedding_model.encode(playlist_descriptions)
        
        # Calculate similarities
        similarities = util.cos_sim(query_embedding, playlist_embeddings)[0]
        
        # Get best match
        best_idx = similarities.argmax().item()
        best_score = float(similarities[best_idx])
        
        return {
            "playlist": playlist_names[best_idx],
            "confidence": best_score,
            "reasoning": f"Selected based on semantic match with {emotion} emotion"
        }
    
    def select_relevant_books(self, emotion: str, emotional_context: str = "", top_k: int = 3) -> List[Dict]:
        """Select multiple relevant philosophy books for comprehensive response"""
        # Create comprehensive query
        query = f"{emotion} emotional guidance wisdom advice {emotional_context}".strip()
        
        # Create embeddings
        query_embedding = self.embedding_model.encode([query])
        
        # Get book embeddings
        book_names = list(self.book_descriptions.keys())
        book_descriptions = [self.book_descriptions[name] for name in book_names]
        book_embeddings = self.embedding_model.encode(book_descriptions)
        
        # Calculate similarities
        similarities = util.cos_sim(query_embedding, book_embeddings)[0]
        
        # Get top matches
        top_indices = similarities.topk(min(top_k, len(similarities))).indices.tolist()
        
        selected_books = []
        for idx in top_indices:
            score = float(similarities[idx])
            if score > 0.2:  # Minimum relevance threshold
                selected_books.append({
                    "book": book_names[idx],
                    "relevance_score": score,
                    "description": self.book_descriptions[book_names[idx]]
                })
        
        return selected_books
    
    def analyze_emotion_complexity(self, text: str, detected_emotion: str) -> Dict:
        """Analyze the complexity and nuance of the emotional expression"""
        text_lower = text.lower()
        
        # Detect emotional complexity indicators
        complexity_indicators = {
            'multiple_emotions': len([word for word in ['and', 'but', 'also', 'yet', 'however'] if word in text_lower]),
            'intensity_words': len([word for word in ['very', 'extremely', 'really', 'so', 'quite'] if word in text_lower]),
            'uncertainty': len([word for word in ['maybe', 'perhaps', 'kind of', 'sort of', 'not sure'] if word in text_lower]),
            'temporal_context': len([word for word in ['today', 'lately', 'recently', 'always', 'never'] if word in text_lower]),
            'social_context': len([word for word in ['people', 'others', 'friends', 'family', 'work'] if word in text_lower])
        }
        
        # Calculate complexity score
        complexity_score = sum(complexity_indicators.values()) / len(text.split())
        
        # Determine if multi-book response is needed
        needs_multi_book = (
            complexity_score > 0.1 or 
            len(text.split()) > 10 or
            complexity_indicators['multiple_emotions'] > 0
        )
        
        return {
            'complexity_score': complexity_score,
            'complexity_indicators': complexity_indicators,
            'needs_multi_book_response': needs_multi_book,
            'recommended_book_count': 3 if needs_multi_book else 1
        }

# Global instance
intelligent_selector = IntelligentSelector()
