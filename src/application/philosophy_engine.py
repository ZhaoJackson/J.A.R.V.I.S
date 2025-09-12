# src/application/philosophy_engine.py - RAG-Enhanced Philosophy Response System

import requests
import json
from typing import Dict, List
from src.commonconst import OLLAMA_URL, OLLAMA_MODEL, OLLAMA_TIMEOUT
from src.application.therapeutic_response import therapeutic_engine

def search_relevant_philosophy(text: str, emotion: str, top_k: int = 5) -> List[Dict]:
    """Search for most relevant philosophy content using RAG"""
    # Ensure embeddings are built
    philosophy_rag.build_embeddings()
    
    # Create comprehensive search query
    search_query = f"{text} {emotion} emotional guidance wisdom advice"
    
    # Search for relevant content
    relevant_content = philosophy_rag.search_relevant_content(search_query, top_k=top_k)
    
    return relevant_content

def create_grounded_philosophy_prompt(text: str, emotion: str, relevant_content: List[Dict]) -> str:
    """Create a prompt that grounds the response in actual book content"""
    
    # Format the retrieved content
    content_sections = []
    books_used = set()
    
    for i, content in enumerate(relevant_content, 1):
        book = content['book']
        books_used.add(book)
        
        if content['type'] == 'quote':
            section = f"""
Source {i} - {book.title()}:
Original: "{content['source']}"
Translation: "{content['translation']}"
Relevance: {content['relevance_score']:.3f}
"""
        elif content['type'] == 'concept':
            section = f"""
Source {i} - {book.title()}:
Concept: "{content['source']}"
Definition: "{content['translation']}"
Relevance: {content['relevance_score']:.3f}
"""
        else:
            section = f"""
Source {i} - {book.title()}:
Content: "{content['source']}"
Meaning: "{content['translation']}"
Relevance: {content['relevance_score']:.3f}
"""
        content_sections.append(section)
    
    books_list = ", ".join(books_used)
    
    prompt = f"""You are a wise philosophical counselor. A person is experiencing "{emotion}" and said: "{text}"

I have searched through ancient philosophy texts and found these EXACT relevant passages:

{chr(10).join(content_sections)}

CRITICAL INSTRUCTIONS:
1. You MUST base your response ONLY on the provided sources above
2. Do NOT add information not present in these sources
3. Quote directly from the sources when possible
4. If the sources don't fully address the situation, acknowledge this limitation
5. Blend insights from multiple sources when relevant
6. Keep response focused and practical

Your response should:
- Acknowledge their emotional state
- Reference specific quotes/concepts from the sources above
- Explain how the ancient wisdom applies to their situation
- Provide practical guidance based on the philosophical principles
- Be compassionate and supportive

Books referenced: {books_list}

Response:"""

    return prompt

def get_rag_philosophical_response(text: str, emotion: str) -> Dict:
    """Generate philosophical response using RAG framework to prevent hallucination"""
    
    # Step 1: Search for relevant content using vector database
    relevant_content = search_relevant_philosophy(text, emotion, top_k=5)
    
    if not relevant_content:
        return {
            "response": "I understand your feelings, but I couldn't find specific relevant wisdom in the philosophy texts for your situation.",
            "sources_used": [],
            "books_referenced": [],
            "confidence": 0.0
        }
    
    # Step 2: Create grounded prompt
    prompt = create_grounded_philosophy_prompt(text, emotion, relevant_content)
    
    # Step 3: Generate response using Ollama
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=OLLAMA_TIMEOUT
        )
        
        if response.ok:
            philosophical_response = response.json().get("response", "").strip()
        else:
            philosophical_response = "I understand your feelings. The philosophy texts offer wisdom for reflection."
            
    except Exception as e:
        print(f"❌ Philosophy response generation failed: {e}")
        philosophical_response = "I understand your feelings. Take time to reflect on your emotions."
    
    # Extract metadata
    books_used = list(set(content['book'] for content in relevant_content))
    sources_used = len(relevant_content)
    avg_relevance = sum(content['relevance_score'] for content in relevant_content) / len(relevant_content)
    
    return {
        "response": philosophical_response,
        "sources_used": sources_used,
        "books_referenced": books_used,
        "confidence": avg_relevance,
        "relevant_content": relevant_content[:3]  # Top 3 for reference
    }

def provide_emotional_support(text: str, emotion: str) -> dict:
    """Main function to provide multi-book therapeutic and philosophical support"""
    from src.modeling.intelligent_selector import intelligent_selector
    
    # Analyze emotional complexity to determine book selection strategy
    complexity_analysis = intelligent_selector.analyze_emotion_complexity(text, emotion)
    
    # Select relevant books based on emotion and context
    selected_books = intelligent_selector.select_relevant_books(
        emotion, 
        text, 
        top_k=complexity_analysis['recommended_book_count']
    )
    
    # Use the advanced therapeutic response engine with multi-book context
    result = therapeutic_engine.generate_integrated_response(text, emotion)
    
    # Format multi-book response
    books_used = [book['book'] for book in selected_books]
    primary_book = books_used[0] if books_used else 'integrated'
    
    # Enhanced response with book attribution
    enhanced_response = result['therapeutic_response']
    if len(books_used) > 1:
        book_list = ", ".join(books_used)
        enhanced_response += f"\n\n📚 This response integrates wisdom from: {book_list}"
    
    return {
        "emotion": emotion,
        "book_used": primary_book,
        "books_referenced": books_used,
        "response": enhanced_response,
        "sources_count": result['sources_count'],
        "confidence": result['confidence'],
        "complexity_analysis": complexity_analysis,
        "selected_books_details": selected_books,
        "psychological_analysis": result.get('psychological_analysis', {}),
        "status": "success"
    }
