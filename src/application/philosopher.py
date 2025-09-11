# src/application/philosopher.py

import json
import requests
from functools import lru_cache
from sentence_transformers import util
from src.commonconst import BOOK_PATHS, OLLAMA_URL, OLLAMA_MODEL, EMBEDDING_MODEL

BOOKS = ["analects", "iching", "mencius", "positive_psy", "social_psy", "tao_te_ching"]

@lru_cache(maxsize=10)
def load_book(book_name: str) -> dict:
    """Load book content from JSON file"""
    with open(BOOK_PATHS[book_name], 'r', encoding='utf-8') as f:
        return json.load(f)

def select_best_book(emotion: str) -> str:
    """Select the most appropriate book based on emotion using semantic similarity"""
    emotion_embedding = EMBEDDING_MODEL.encode(emotion, convert_to_tensor=True)
    book_embeddings = EMBEDDING_MODEL.encode(BOOKS, convert_to_tensor=True)
    
    scores = util.cos_sim(emotion_embedding, book_embeddings)[0]
    best_index = scores.argmax().item()
    return BOOKS[best_index]

def extract_relevant_quotes(book_data: dict, emotion: str, limit: int = 3) -> list:
    """Extract most relevant quotes from book based on emotion"""
    quotes = []
    
    # Handle different book structures
    if isinstance(book_data, list):
        for item in book_data:
            if isinstance(item, dict):
                if 'entries' in item:  # analects structure
                    quotes.extend(item['entries'])
                elif 'contents' in item:  # mencius structure
                    quotes.extend(item['contents'])
                elif 'source' in item:  # direct quote structure
                    quotes.append(item)
    elif isinstance(book_data, dict):
        # positive_psy or social_psy structure
        for category in book_data.values():
            if isinstance(category, dict) and 'concepts' in category:
                quotes.extend(category['concepts'])
    
    if not quotes:
        return []
    
    # Score quotes based on emotion similarity
    quote_texts = []
    for quote in quotes[:50]:  # Limit to first 50 for performance
        if 'source' in quote:
            quote_texts.append(quote.get('source', ''))
        elif 'term' in quote:
            quote_texts.append(quote.get('term', ''))
        else:
            quote_texts.append(str(quote))
    
    if not quote_texts:
        return quotes[:limit]
    
    emotion_embedding = EMBEDDING_MODEL.encode(emotion, convert_to_tensor=True)
    quote_embeddings = EMBEDDING_MODEL.encode(quote_texts, convert_to_tensor=True)
    
    scores = util.cos_sim(emotion_embedding, quote_embeddings)[0]
    best_indices = scores.topk(min(limit, len(quotes))).indices.tolist()
    
    return [quotes[i] for i in best_indices]

def get_philosophical_response(text: str, emotion: str) -> str:
    """Generate philosophical response using Ollama"""
    book_name = select_best_book(emotion)
    book_data = load_book(book_name)
    relevant_quotes = extract_relevant_quotes(book_data, emotion, 2)
    
    # Format quotes for prompt
    quote_text = ""
    for i, quote in enumerate(relevant_quotes, 1):
        if 'source' in quote and 'target' in quote:
            quote_text += f"{i}. Original: {quote['source']}\n   Translation: {quote['target']}\n\n"
        elif 'term' in quote and 'definition' in quote:
            quote_text += f"{i}. {quote['term']}: {quote['definition']}\n\n"
        else:
            quote_text += f"{i}. {str(quote)}\n\n"
    
    prompt = f"""You are a wise philosophical advisor. A person is feeling "{emotion}" and said: "{text}"

Here are relevant quotes from {book_name}:
{quote_text}

Provide a compassionate response that:
1. Acknowledges their emotion
2. Relates one of the quotes to their situation  
3. Offers practical wisdom
4. Keeps it concise (2-3 paragraphs)

Response:"""

    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
        timeout=30
    )
    
    if response.ok:
        return response.json().get("response", "I understand how you're feeling. Take time to reflect on your emotions.")
    return "I understand how you're feeling. Take time to reflect on your emotions."

def provide_emotional_support(text: str, emotion: str) -> dict:
    """Main function to provide philosophical emotional support"""
    book_name = select_best_book(emotion)
    philosophical_response = get_philosophical_response(text, emotion)
    
    return {
        "emotion": emotion,
        "book_used": book_name,
        "response": philosophical_response,
        "status": "success"
    }
