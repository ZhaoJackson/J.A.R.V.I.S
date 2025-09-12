# src/application/psychology_prompts.py - Sophisticated Psychology Domain Prompts

from typing import Dict, List

class PsychologyPromptEngine:
    """Advanced prompt engineering for psychological analysis and therapeutic responses"""
    
    def __init__(self):
        self.clinical_frameworks = {
            'cognitive_behavioral': {
                'focus': 'thoughts, behaviors, and emotions interconnection',
                'approach': 'identifying and challenging negative thought patterns',
                'techniques': ['thought_challenging', 'behavioral_activation', 'exposure_therapy']
            },
            'humanistic': {
                'focus': 'self-acceptance, personal growth, and inherent worth',
                'approach': 'unconditional positive regard and empathetic understanding',
                'techniques': ['active_listening', 'reflection', 'validation']
            },
            'mindfulness_based': {
                'focus': 'present-moment awareness and acceptance',
                'approach': 'observing thoughts and emotions without judgment',
                'techniques': ['meditation', 'breathing_exercises', 'body_awareness']
            }
        }
    
    def create_emotion_analysis_prompt(self, text: str, context: Dict = None) -> str:
        """Create sophisticated emotion analysis prompt"""
        
        base_prompt = f"""You are a licensed clinical psychologist with expertise in emotion regulation and psychological assessment.

PATIENT EXPRESSION: "{text}"

Conduct a comprehensive psychological assessment following these frameworks:

1. EMOTIONAL ASSESSMENT:
   - Primary emotion and intensity (1-10 scale)
   - Secondary emotions present
   - Emotional regulation patterns
   - Affect stability indicators

2. COGNITIVE ANALYSIS:
   - Thought patterns (rational vs. irrational)
   - Cognitive distortions present
   - Metacognitive awareness level
   - Problem-solving orientation

3. BEHAVIORAL INDICATORS:
   - Implied behavioral patterns
   - Coping mechanisms used
   - Social functioning indicators
   - Activity level implications

4. PSYCHOLOGICAL NEEDS:
   - Maslow's hierarchy level
   - Attachment style indicators
   - Self-efficacy beliefs
   - Autonomy vs. dependency needs

5. THERAPEUTIC RECOMMENDATIONS:
   - Most suitable therapeutic approach
   - Specific intervention techniques
   - Crisis risk assessment (low/medium/high)
   - Support system recommendations

Respond in JSON format with detailed clinical observations:

{{
    "emotional_assessment": {{
        "primary_emotion": "emotion name",
        "intensity": "1-10 scale",
        "secondary_emotions": ["list"],
        "regulation_pattern": "description"
    }},
    "cognitive_analysis": {{
        "thought_patterns": "description",
        "cognitive_distortions": ["list"],
        "metacognitive_level": "low/medium/high"
    }},
    "psychological_needs": {{
        "primary_needs": ["list"],
        "hierarchy_level": "physiological/safety/love/esteem/self-actualization",
        "attachment_indicators": "description"
    }},
    "therapeutic_recommendations": {{
        "approach": "CBT/humanistic/mindfulness/integrated",
        "techniques": ["list"],
        "crisis_level": "low/medium/high",
        "support_type": "description"
    }},
    "clinical_summary": "brief professional assessment"
}}"""

        return base_prompt
    
    def create_rag_philosophy_prompt(self, text: str, emotion: str, sources: List[Dict]) -> str:
        """Create RAG-enhanced philosophy prompt with multi-book integration"""
        
        # Group sources by book
        sources_by_book = {}
        for source in sources:
            book = source['book']
            if book not in sources_by_book:
                sources_by_book[book] = []
            sources_by_book[book].append(source)
        
        # Format sources with attribution
        formatted_sources = []
        for book, book_sources in sources_by_book.items():
            book_section = f"\n=== {book.upper()} PHILOSOPHY ===\n"
            for i, source in enumerate(book_sources, 1):
                book_section += f"""
Source {i} (Relevance: {source['relevance_score']:.3f}):
Original: "{source['source']}"
Translation/Meaning: "{source['translation']}"
Type: {source['type']}
"""
            formatted_sources.append(book_section)
        
        books_referenced = list(sources_by_book.keys())
        
        prompt = f"""You are a wise philosophical counselor with deep knowledge of ancient wisdom traditions and modern psychology.

SITUATION:
A person experiencing "{emotion}" has shared: "{text}"

RETRIEVED PHILOSOPHICAL SOURCES:
{chr(10).join(formatted_sources)}

THERAPEUTIC GUIDELINES:
1. Ground ALL advice in the provided sources above - do NOT add external information
2. Quote directly from sources and cite which book each quote comes from
3. Blend insights from multiple philosophical traditions when relevant
4. Connect ancient wisdom to their modern emotional experience
5. Provide practical, actionable guidance
6. Acknowledge limitations if sources don't fully address their situation

RESPONSE STRUCTURE:
1. Emotional Acknowledgment (validate their feelings)
2. Philosophical Insights (cite specific sources with book attribution)
3. Practical Wisdom (actionable advice based on the sources)
4. Integration (how different philosophical traditions complement each other)

CITATION FORMAT:
- "As the Analects teaches us: '[quote]'"
- "The I Ching wisdom suggests: '[quote]'"
- "Modern psychology principles indicate: '[concept]'"

CRITICAL: Only use information from the sources provided above. If the sources don't address their specific situation, acknowledge this honestly.

Books Referenced: {', '.join(books_referenced)}
Total Sources: {len(sources)}

Philosophical Response:"""

        return prompt
    
    def create_therapeutic_response_prompt(self, text: str, psychological_analysis: Dict, philosophy_sources: List[Dict]) -> str:
        """Create integrated therapeutic response combining psychology and philosophy"""
        
        primary_emotion = psychological_analysis.get('emotional_assessment', {}).get('primary_emotion', 'unknown')
        intensity = psychological_analysis.get('emotional_assessment', {}).get('intensity', 'medium')
        needs = psychological_analysis.get('psychological_needs', {}).get('primary_needs', [])
        approach = psychological_analysis.get('therapeutic_recommendations', {}).get('approach', 'integrated')
        
        # Format philosophy sources
        philosophy_text = ""
        for i, source in enumerate(philosophy_sources[:3], 1):
            philosophy_text += f"\n{i}. From {source['book']}: \"{source['source']}\" - {source['translation']}\n"
        
        prompt = f"""You are an integrative therapist combining clinical psychology with philosophical wisdom.

CLIENT PRESENTATION: "{text}"

PSYCHOLOGICAL ASSESSMENT:
- Primary Emotion: {primary_emotion} (Intensity: {intensity}/10)
- Psychological Needs: {', '.join(needs)}
- Recommended Approach: {approach}

RELEVANT PHILOSOPHICAL WISDOM:
{philosophy_text}

Create a therapeutic response that:

1. VALIDATES their emotional experience with clinical understanding
2. INTEGRATES ancient philosophical wisdom with modern psychological principles
3. PROVIDES specific, actionable coping strategies
4. CONNECTS their current experience to universal human wisdom
5. OFFERS hope and practical next steps

Keep the response:
- Compassionate and non-judgmental
- Grounded in both psychology and philosophy
- Practical and actionable
- Appropriate for their emotional intensity level
- Limited to 3-4 paragraphs

Therapeutic Response:"""

        return prompt

# Global instance
psychology_prompts = PsychologyPromptEngine()
