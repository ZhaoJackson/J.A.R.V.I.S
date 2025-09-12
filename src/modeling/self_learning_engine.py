# src/modeling/self_learning_engine.py - Reinforcement Learning from User Interactions

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from collections import defaultdict
from datetime import datetime, timedelta
from sentence_transformers import util
import pickle
from src.commonconst import CSV_EXPORT_PATH, DB_DIR, EMBEDDING_MODEL

class SelfLearningEngine:
    """Self-improving system that learns from user interactions"""
    
    def __init__(self):
        self.embedding_model = EMBEDDING_MODEL
        self.learning_cache_path = DB_DIR / "learning_patterns.pkl"
        self.user_patterns = defaultdict(list)
        self.emotion_patterns = defaultdict(list)
        self.book_effectiveness = defaultdict(float)
        self.playlist_effectiveness = defaultdict(float)
        
    def load_user_interaction_data(self) -> pd.DataFrame:
        """Load and analyze user interaction patterns from CSV"""
        try:
            df = pd.read_csv(CSV_EXPORT_PATH)
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            return df.sort_values('Timestamp')
        except Exception as e:
            print(f"📊 No interaction data found: {e}")
            return pd.DataFrame()
    
    def analyze_user_patterns(self) -> Dict:
        """Analyze user's emotional patterns and preferences"""
        df = self.load_user_interaction_data()
        
        if df.empty:
            return {"status": "no_data"}
        
        patterns = {}
        
        # Emotion frequency analysis
        emotion_counts = df['Detected Emotion'].value_counts()
        patterns['most_common_emotions'] = emotion_counts.head(5).to_dict()
        
        # Book preference analysis
        book_counts = df['Philosophy Book'].value_counts()
        patterns['preferred_books'] = book_counts.head(3).to_dict()
        
        # Time-based patterns
        df['Hour'] = df['Timestamp'].dt.hour
        hourly_patterns = df['Hour'].value_counts().sort_index()
        patterns['active_hours'] = hourly_patterns.to_dict()
        
        # Recent vs historical emotions (last 7 days)
        recent_cutoff = datetime.now() - timedelta(days=7)
        recent_df = df[df['Timestamp'] > recent_cutoff]
        
        if not recent_df.empty:
            patterns['recent_emotions'] = recent_df['Detected Emotion'].value_counts().to_dict()
            patterns['emotional_trend'] = self.analyze_emotional_trend(recent_df)
        
        # Session patterns by user
        user_sessions = df.groupby('Session ID').agg({
            'Detected Emotion': 'count',
            'Philosophy Book': lambda x: x.mode().iloc[0] if not x.empty else 'none'
        }).to_dict()
        
        patterns['user_preferences'] = user_sessions
        
        return patterns
    
    def analyze_emotional_trend(self, recent_df: pd.DataFrame) -> str:
        """Analyze if user's emotions are trending positive/negative/stable"""
        if len(recent_df) < 3:
            return "insufficient_data"
        
        # Simple sentiment scoring
        emotion_scores = {
            'joy': 1.0, 'gratitude': 0.8, 'calm': 0.6, 'excitement': 0.9,
            'sadness': -0.8, 'anxiety': -0.6, 'anger': -0.9, 'confusion': -0.3,
            'loneliness': -0.7, 'overwhelm': -0.5
        }
        
        recent_df['emotion_score'] = recent_df['Detected Emotion'].str.lower().map(emotion_scores).fillna(0)
        
        # Calculate trend
        scores = recent_df['emotion_score'].values
        if len(scores) >= 3:
            trend = np.polyfit(range(len(scores)), scores, 1)[0]
            if trend > 0.1:
                return "improving"
            elif trend < -0.1:
                return "declining"
            else:
                return "stable"
        
        return "stable"
    
    def learn_from_interactions(self) -> Dict:
        """Learn patterns from user interactions to improve future responses"""
        patterns = self.analyze_user_patterns()
        
        if patterns.get("status") == "no_data":
            return {"learning_status": "no_data", "recommendations": []}
        
        learning_insights = {}
        
        # Learn emotion-book effectiveness
        df = self.load_user_interaction_data()
        
        # Group by emotion and see which books are most used
        emotion_book_pairs = df.groupby(['Detected Emotion', 'Philosophy Book']).size().reset_index(name='count')
        
        for _, row in emotion_book_pairs.iterrows():
            emotion = row['Detected Emotion'].lower()
            book = row['Philosophy Book']
            count = row['count']
            
            # Higher count = more effective for this emotion
            effectiveness_key = f"{emotion}_{book}"
            self.book_effectiveness[effectiveness_key] = count
        
        # Learn emotion-playlist effectiveness
        emotion_playlist_pairs = df.groupby(['Detected Emotion', 'Music Playlist']).size().reset_index(name='count')
        
        for _, row in emotion_playlist_pairs.iterrows():
            emotion = row['Detected Emotion'].lower()
            playlist = row['Music Playlist']
            count = row['count']
            
            effectiveness_key = f"{emotion}_{playlist}"
            self.playlist_effectiveness[effectiveness_key] = count
        
        # Generate personalized recommendations
        recommendations = self.generate_personalized_recommendations(patterns)
        
        learning_insights = {
            "total_interactions": len(df),
            "learning_patterns": patterns,
            "book_effectiveness": dict(self.book_effectiveness),
            "playlist_effectiveness": dict(self.playlist_effectiveness),
            "personalized_recommendations": recommendations,
            "last_updated": datetime.now().isoformat()
        }
        
        # Cache learning insights
        with open(self.learning_cache_path, 'wb') as f:
            pickle.dump(learning_insights, f)
        
        print(f"📈 Learning complete: {len(df)} interactions analyzed")
        return learning_insights
    
    def generate_personalized_recommendations(self, patterns: Dict) -> List[str]:
        """Generate personalized recommendations based on learned patterns"""
        recommendations = []
        
        # Emotion-based recommendations
        if 'most_common_emotions' in patterns:
            top_emotion = list(patterns['most_common_emotions'].keys())[0]
            recommendations.append(f"You frequently experience {top_emotion} - consider exploring coping strategies for this emotion")
        
        # Book preference recommendations
        if 'preferred_books' in patterns:
            preferred_book = list(patterns['preferred_books'].keys())[0]
            recommendations.append(f"You resonate with {preferred_book} philosophy - consider deeper study of this tradition")
        
        # Trend-based recommendations
        if 'emotional_trend' in patterns:
            trend = patterns['emotional_trend']
            if trend == "improving":
                recommendations.append("Your emotional state is trending positive - continue current practices")
            elif trend == "declining":
                recommendations.append("Consider additional support - your emotional trend suggests need for extra care")
        
        return recommendations
    
    def get_learned_preferences(self, emotion: str) -> Dict:
        """Get learned preferences for a specific emotion"""
        try:
            with open(self.learning_cache_path, 'rb') as f:
                learning_data = pickle.load(f)
        except:
            learning_data = self.learn_from_interactions()
        
        emotion_lower = emotion.lower()
        
        # Find most effective book for this emotion
        book_scores = {}
        for key, score in learning_data.get('book_effectiveness', {}).items():
            if key.startswith(f"{emotion_lower}_"):
                book = key.replace(f"{emotion_lower}_", "")
                book_scores[book] = score
        
        # Find most effective playlist for this emotion
        playlist_scores = {}
        for key, score in learning_data.get('playlist_effectiveness', {}).items():
            if key.startswith(f"{emotion_lower}_"):
                playlist = key.replace(f"{emotion_lower}_", "")
                playlist_scores[playlist] = score
        
        return {
            "preferred_books": sorted(book_scores.items(), key=lambda x: x[1], reverse=True),
            "preferred_playlists": sorted(playlist_scores.items(), key=lambda x: x[1], reverse=True),
            "learning_confidence": min(sum(book_scores.values()) + sum(playlist_scores.values()), 10) / 10
        }
    
    def update_learning_from_new_interaction(self, user_input: str, emotion: str, book_used: str, playlist_used: str):
        """Update learning patterns with new interaction (called after each response)"""
        # This creates a feedback loop - each interaction improves the model
        
        # Load existing patterns
        try:
            with open(self.learning_cache_path, 'rb') as f:
                learning_data = pickle.load(f)
        except:
            learning_data = {"book_effectiveness": {}, "playlist_effectiveness": {}}
        
        # Update effectiveness scores
        emotion_lower = emotion.lower()
        book_key = f"{emotion_lower}_{book_used}"
        playlist_key = f"{emotion_lower}_{playlist_used}"
        
        # Increment effectiveness (positive reinforcement)
        learning_data["book_effectiveness"][book_key] = learning_data["book_effectiveness"].get(book_key, 0) + 1
        learning_data["playlist_effectiveness"][playlist_key] = learning_data["playlist_effectiveness"].get(playlist_key, 0) + 1
        
        # Save updated patterns
        with open(self.learning_cache_path, 'wb') as f:
            pickle.dump(learning_data, f)
        
        print(f"📈 Learning updated: {emotion} → {book_used} + {playlist_used}")

# Global instance
self_learning_engine = SelfLearningEngine()
