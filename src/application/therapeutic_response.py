# src/application/therapeutic_response.py - Integrated Therapeutic Response System

import requests
import json
from typing import Dict, List
from src.commonconst import OLLAMA_URL, OLLAMA_MODEL, OLLAMA_TIMEOUT
from src.application.psychology_prompts import psychology_prompts
from src.vector_space.philosophy_rag import philosophy_rag

class TherapeuticResponseEngine:
    """Integrated system combining psychological analysis with philosophical wisdom"""
    
    def __init__(self):
        self.psychology_prompts = psychology_prompts
        self.philosophy_rag = philosophy_rag
    
    def generate_psychological_analysis(self, text: str) -> Dict:
        """Generate comprehensive psychological analysis"""
        prompt = self.psychology_prompts.create_emotion_analysis_prompt(text)
        
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
                        return json.loads(json_match.group(0))
                    except json.JSONDecodeError:
                        pass
            
            # Fallback
            return self.create_fallback_psychological_analysis(text)
            
        except Exception as e:
            print(f"❌ Psychological analysis failed: {e}")
            return self.create_fallback_psychological_analysis(text)
    
    def create_fallback_psychological_analysis(self, text: str) -> Dict:
        """Create fallback psychological analysis"""
        return {
            "emotional_assessment": {
                "primary_emotion": "mixed",
                "intensity": "5",
                "secondary_emotions": [],
                "regulation_pattern": "seeking support"
            },
            "cognitive_analysis": {
                "thought_patterns": "processing current experience",
                "cognitive_distortions": [],
                "metacognitive_level": "medium"
            },
            "psychological_needs": {
                "primary_needs": ["understanding", "support", "guidance"],
                "hierarchy_level": "love",
                "attachment_indicators": "seeking connection"
            },
            "therapeutic_recommendations": {
                "approach": "humanistic",
                "techniques": ["active_listening", "validation", "reflection"],
                "crisis_level": "low",
                "support_type": "empathetic guidance"
            },
            "clinical_summary": "Individual seeking emotional support and guidance"
        }
    
    def search_multi_book_philosophy(self, text: str, emotion: str, top_k: int = 8) -> List[Dict]:
        """Search across all philosophy books for relevant content"""
        # Ensure embeddings are built
        self.philosophy_rag.build_embeddings()
        
        # Create comprehensive search queries
        search_queries = [
            f"{text} {emotion}",
            f"emotional guidance {emotion}",
            f"wisdom advice {emotion}",
            f"philosophical support {emotion}"
        ]
        
        all_results = []
        seen_sources = set()
        
        for query in search_queries:
            results = self.philosophy_rag.search_relevant_content(query, top_k=top_k//len(search_queries))
            
            for result in results:
                # Avoid duplicate sources
                source_key = f"{result['book']}_{result['source'][:50]}"
                if source_key not in seen_sources:
                    all_results.append(result)
                    seen_sources.add(source_key)
        
        # Sort by relevance score and return top results
        all_results.sort(key=lambda x: x['relevance_score'], reverse=True)
        return all_results[:top_k]
    
    def generate_integrated_response(self, text: str, emotion: str) -> Dict:
        """Generate integrated therapeutic response combining psychology and philosophy"""
        
        # Step 1: Psychological analysis
        psychological_analysis = self.generate_psychological_analysis(text)
        
        # Step 2: Search philosophy across all books
        philosophy_sources = self.search_multi_book_philosophy(text, emotion, top_k=6)
        
        # Step 3: Generate integrated therapeutic response
        if philosophy_sources:
            prompt = self.psychology_prompts.create_therapeutic_response_prompt(
                text, psychological_analysis, philosophy_sources
            )
            
            try:
                response = requests.post(
                    f"{OLLAMA_URL}/api/generate",
                    json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
                    timeout=OLLAMA_TIMEOUT
                )
                
                if response.ok:
                    therapeutic_response = response.json().get("response", "").strip()
                else:
                    therapeutic_response = "I understand your feelings and am here to support you."
                    
            except Exception as e:
                print(f"❌ Therapeutic response generation failed: {e}")
                therapeutic_response = "I understand your feelings and am here to support you."
        else:
            therapeutic_response = "I understand your feelings. While I couldn't find specific philosophical guidance for your situation, know that your emotions are valid and seeking support is a sign of strength."
        
        # Extract books used
        books_used = list(set(source['book'] for source in philosophy_sources))
        
        return {
            "emotion": emotion,
            "psychological_analysis": psychological_analysis,
            "therapeutic_response": therapeutic_response,
            "philosophy_sources": philosophy_sources,
            "books_referenced": books_used,
            "sources_count": len(philosophy_sources),
            "confidence": sum(s['relevance_score'] for s in philosophy_sources) / len(philosophy_sources) if philosophy_sources else 0.0,
            "status": "success"
        }

# Global instance
therapeutic_engine = TherapeuticResponseEngine()
