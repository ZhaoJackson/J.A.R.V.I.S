# src/application/emotion_engine.py - Advanced Emotion Analysis with Psychological Insights

import requests
import json
from typing import Dict, Tuple
from src.commonconst import OLLAMA_URL, OLLAMA_MODEL, OLLAMA_TIMEOUT
from src.modeling.simple_emotion_model import simple_emotion_classifier

def analyze_emotion_with_psychology(text: str) -> Dict:
    """
    Advanced emotion analysis combining NLP model and psychological assessment
    """
    # Step 1: Use hybrid emotion classification
    classification_result = simple_emotion_classifier.classify_emotion_hybrid(text)
    primary_emotion = classification_result['primary_emotion']
    confidence = classification_result['confidence']
    
    # Step 3: Use Ollama for deeper psychological analysis
    psychological_analysis = get_psychological_analysis(text, primary_emotion)
    
    return {
        'primary_emotion': primary_emotion,
        'confidence': confidence,
        'psychological_analysis': psychological_analysis,
        'classification_details': classification_result,
        'status': 'success'
    }

def get_psychological_analysis(text: str, detected_emotion: str) -> Dict:
    """Generate deep psychological analysis using Ollama"""
    
    prompt = f"""You are a clinical psychologist with expertise in emotion analysis. 
    
A person has expressed: "{text}"
Initial emotion detected: {detected_emotion}

Please provide a comprehensive psychological analysis in JSON format:

{{
    "emotional_state": "primary emotion (one word)",
    "intensity": "low/medium/high",
    "emotional_triggers": ["list", "of", "potential", "triggers"],
    "underlying_needs": ["list", "of", "psychological", "needs"],
    "coping_strategies": ["list", "of", "healthy", "coping", "methods"],
    "psychological_pattern": "brief description of emotional pattern",
    "support_recommendation": "type of support most beneficial"
}}

Focus on:
1. Emotional intensity and nuance
2. Underlying psychological needs
3. Healthy coping mechanisms
4. Pattern recognition
5. Support recommendations

Respond ONLY with valid JSON, no additional text."""

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=OLLAMA_TIMEOUT
        )
        
        if response.ok:
            raw_response = response.json().get("response", "").strip()
            
            # Extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
            if json_match:
                try:
                    psychological_data = json.loads(json_match.group(0))
                    return psychological_data
                except json.JSONDecodeError:
                    pass
        
        # Fallback if JSON parsing fails
        return create_fallback_analysis(detected_emotion)
        
    except Exception as e:
        print(f"❌ Psychological analysis failed: {e}")
        return create_fallback_analysis(detected_emotion)

def create_fallback_analysis(emotion: str) -> Dict:
    """Create fallback psychological analysis"""
    fallback_data = {
        'joy': {
            "emotional_state": "joy",
            "intensity": "medium",
            "emotional_triggers": ["positive events", "achievements", "social connection"],
            "underlying_needs": ["celebration", "sharing", "connection"],
            "coping_strategies": ["savor the moment", "share with others", "practice gratitude"],
            "psychological_pattern": "positive emotional state with high energy",
            "support_recommendation": "social connection and celebration"
        },
        'anxiety': {
            "emotional_state": "anxiety",
            "intensity": "medium",
            "emotional_triggers": ["uncertainty", "future events", "performance pressure"],
            "underlying_needs": ["security", "control", "reassurance"],
            "coping_strategies": ["deep breathing", "planning", "mindfulness", "grounding techniques"],
            "psychological_pattern": "worry about future outcomes",
            "support_recommendation": "calming techniques and structured support"
        },
        'sadness': {
            "emotional_state": "sadness",
            "intensity": "medium",
            "emotional_triggers": ["loss", "disappointment", "rejection"],
            "underlying_needs": ["comfort", "understanding", "healing"],
            "coping_strategies": ["self-compassion", "emotional expression", "social support"],
            "psychological_pattern": "processing difficult emotions",
            "support_recommendation": "empathetic listening and gentle guidance"
        }
    }
    
    return fallback_data.get(emotion, fallback_data['anxiety'])

def analyze_emotion(text: str) -> str:
    """Simple emotion analysis for backward compatibility"""
    result = analyze_emotion_with_psychology(text)
    return result['primary_emotion']

def get_emotion_analysis_summary(text: str) -> str:
    """Get a human-readable summary of emotion analysis"""
    analysis = analyze_emotion_with_psychology(text)
    
    summary = f"""
🧠 Emotion Analysis Summary:
• Primary Emotion: {analysis['primary_emotion']} ({analysis['confidence']:.2f} confidence)
• Intensity: {analysis['psychological_analysis'].get('intensity', 'medium')}
• Key Triggers: {', '.join(analysis['psychological_analysis'].get('emotional_triggers', []))}
• Coping Strategies: {', '.join(analysis['psychological_analysis'].get('coping_strategies', []))}
• Support Needed: {analysis['psychological_analysis'].get('support_recommendation', 'general support')}
"""
    return summary.strip()
