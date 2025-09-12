# src/modeling/simple_emotion_model.py - Robust Emotion Classification

import requests
from typing import Dict, List, Tuple
from sentence_transformers import util
from src.commonconst import OLLAMA_URL, OLLAMA_MODEL, OLLAMA_TIMEOUT, EMBEDDING_MODEL

class SimpleEmotionClassifier:
    """Simple but effective emotion classifier using semantic similarity and LLM"""
    
    def __init__(self):
        self.embedding_model = EMBEDDING_MODEL
        
        # Core emotion categories with rich descriptions
        self.emotion_profiles = {
            'joy': {
                'keywords': ['happy', 'joyful', 'excited', 'thrilled', 'elated', 'cheerful', 'delighted', 'euphoric'],
                'description': 'positive high-energy emotions characterized by happiness, excitement, and celebration',
                'psychological_markers': ['achievement', 'success', 'social_connection', 'positive_events']
            },
            'sadness': {
                'keywords': ['sad', 'depressed', 'melancholy', 'sorrowful', 'gloomy', 'downcast', 'dejected'],
                'description': 'low-energy emotions involving loss, disappointment, or grief',
                'psychological_markers': ['loss', 'rejection', 'failure', 'separation', 'disappointment']
            },
            'anxiety': {
                'keywords': ['anxious', 'worried', 'nervous', 'stressed', 'fearful', 'apprehensive', 'tense'],
                'description': 'future-focused emotions involving worry, fear, and anticipation of threat',
                'psychological_markers': ['uncertainty', 'threat', 'performance', 'future_events', 'unknown_outcomes']
            },
            'anger': {
                'keywords': ['angry', 'furious', 'frustrated', 'irritated', 'annoyed', 'enraged', 'livid'],
                'description': 'high-energy emotions involving frustration, injustice, or obstruction',
                'psychological_markers': ['injustice', 'obstruction', 'disrespect', 'violation', 'blocked_goals']
            },
            'calm': {
                'keywords': ['calm', 'peaceful', 'serene', 'tranquil', 'relaxed', 'composed', 'centered'],
                'description': 'balanced emotions characterized by peace, stability, and inner harmony',
                'psychological_markers': ['acceptance', 'resolution', 'mindfulness', 'balance', 'clarity']
            },
            'confusion': {
                'keywords': ['confused', 'uncertain', 'lost', 'unclear', 'bewildered', 'perplexed'],
                'description': 'cognitive-emotional state involving uncertainty and lack of clarity',
                'psychological_markers': ['ambiguity', 'complexity', 'decision_making', 'unclear_path']
            },
            'gratitude': {
                'keywords': ['grateful', 'thankful', 'appreciative', 'blessed', 'content'],
                'description': 'positive emotions focused on appreciation and recognition of benefits',
                'psychological_markers': ['recognition', 'appreciation', 'social_support', 'positive_reflection']
            },
            'loneliness': {
                'keywords': ['lonely', 'isolated', 'alone', 'disconnected', 'solitary'],
                'description': 'social-emotional state involving lack of connection and belonging',
                'psychological_markers': ['social_isolation', 'disconnection', 'lack_of_belonging', 'social_needs']
            }
        }
    
    def classify_emotion_semantic(self, text: str) -> Dict:
        """Classify emotion using semantic similarity"""
        text_embedding = self.embedding_model.encode([text])
        
        emotion_scores = {}
        
        for emotion, profile in self.emotion_profiles.items():
            # Create comprehensive emotion description
            emotion_description = f"{' '.join(profile['keywords'])} {profile['description']} {' '.join(profile['psychological_markers'])}"
            
            # Calculate similarity
            emotion_embedding = self.embedding_model.encode([emotion_description])
            similarity = util.cos_sim(text_embedding, emotion_embedding)[0][0].item()
            
            emotion_scores[emotion] = similarity
        
        # Get top emotions
        sorted_emotions = sorted(emotion_scores.items(), key=lambda x: x[1], reverse=True)
        
        primary_emotion = sorted_emotions[0][0]
        confidence = sorted_emotions[0][1]
        
        return {
            'primary_emotion': primary_emotion,
            'confidence': confidence,
            'top_emotions': sorted_emotions[:3],
            'all_scores': emotion_scores
        }
    
    def classify_emotion_llm(self, text: str) -> Dict:
        """Use LLM for sophisticated emotion classification"""
        
        emotion_list = list(self.emotion_profiles.keys())
        emotion_descriptions = {k: v['description'] for k, v in self.emotion_profiles.items()}
        
        prompt = f"""You are a clinical psychologist specializing in emotion classification.

Analyze this emotional expression: "{text}"

Available emotion categories:
{chr(10).join([f"- {emotion}: {desc}" for emotion, desc in emotion_descriptions.items()])}

Provide a detailed analysis in JSON format:

{{
    "primary_emotion": "main emotion from the list above",
    "confidence": "0.0-1.0 confidence score",
    "secondary_emotions": ["list of other relevant emotions"],
    "emotional_intensity": "low/medium/high",
    "emotional_complexity": "simple/moderate/complex",
    "psychological_indicators": ["list of psychological markers present"],
    "reasoning": "brief explanation of classification"
}}

Focus on psychological accuracy and nuance. Respond ONLY with valid JSON."""

        try:
            response = requests.post(
                f"{OLLAMA_URL}/api/generate",
                json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
                timeout=OLLAMA_TIMEOUT
            )
            
            if response.ok:
                raw_response = response.json().get("response", "").strip()
                
                # Extract JSON
                import re
                json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
                if json_match:
                    try:
                        import json
                        return json.loads(json_match.group(0))
                    except json.JSONDecodeError:
                        pass
            
            # Fallback to semantic classification
            return self.classify_emotion_semantic(text)
            
        except Exception as e:
            print(f"❌ LLM classification failed: {e}")
            return self.classify_emotion_semantic(text)
    
    def classify_emotion_hybrid(self, text: str) -> Dict:
        """Hybrid approach combining semantic similarity and LLM analysis"""
        
        # Get both classifications
        semantic_result = self.classify_emotion_semantic(text)
        llm_result = self.classify_emotion_llm(text)
        
        # Use LLM result if available and confident, otherwise semantic
        if isinstance(llm_result, dict) and 'primary_emotion' in llm_result:
            llm_confidence = llm_result.get('confidence', 0.5)
            if isinstance(llm_confidence, str):
                try:
                    llm_confidence = float(llm_confidence)
                except:
                    llm_confidence = 0.5
            
            # Combine results
            return {
                'primary_emotion': llm_result['primary_emotion'],
                'confidence': llm_confidence,
                'semantic_backup': semantic_result,
                'llm_analysis': llm_result,
                'method': 'hybrid_llm'
            }
        else:
            return {
                'primary_emotion': semantic_result['primary_emotion'],
                'confidence': semantic_result['confidence'],
                'semantic_analysis': semantic_result,
                'method': 'semantic_fallback'
            }

# Global instance
simple_emotion_classifier = SimpleEmotionClassifier()
