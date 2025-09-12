# src/application/philosophy_rag.py - Simple RAG System for Philosophy Books

import json
import pickle
from pathlib import Path
from typing import List, Dict
from sentence_transformers import util
from src.commonconst import BOOK_PATHS, EMBEDDING_MODEL, DB_DIR

class SimplePhilosophyRAG:
    """Simple RAG system using sentence transformers without FAISS"""
    
    def __init__(self):
        self.model = EMBEDDING_MODEL
        self.content_cache_path = DB_DIR / "philosophy_content.pkl"
        self.embeddings_cache_path = DB_DIR / "philosophy_embeddings.pkl"
        self.content_data = []
        self.embeddings = None
        
    def extract_all_content(self) -> List[Dict]:
        """Extract all content from philosophy books"""
        all_content = []
        
        for book_name, book_path in BOOK_PATHS.items():
            print(f"📖 Processing {book_name}...")
            
            with open(book_path, 'r', encoding='utf-8') as f:
                book_data = json.load(f)
            
            # Handle different book structures
            if book_name == "analects":
                for book_section in book_data:
                    if isinstance(book_section, dict) and 'entries' in book_section:
                        for entry in book_section['entries']:
                            if 'source' in entry and 'target' in entry:
                                all_content.append({
                                    'text': f"{entry['source']} {entry['target']}",
                                    'source': entry['source'],
                                    'translation': entry['target'],
                                    'book': book_name,
                                    'type': 'quote'
                                })
                                
            elif book_name == "mencius":
                for chapter in book_data:
                    if isinstance(chapter, dict) and 'contents' in chapter:
                        for content in chapter['contents']:
                            if 'source' in content and 'target' in content:
                                all_content.append({
                                    'text': f"{content['source']} {content['target']}",
                                    'source': content['source'],
                                    'translation': content['target'],
                                    'book': book_name,
                                    'type': 'quote'
                                })
                                
            elif book_name == "tao_te_ching":
                for chapter in book_data:
                    if isinstance(chapter, dict):
                        original = chapter.get('original', '')
                        translation = chapter.get('translation', '')
                        if original and translation:
                            all_content.append({
                                'text': f"{original} {translation}",
                                'source': original,
                                'translation': translation,
                                'book': book_name,
                                'chapter': chapter.get('chapter_number', ''),
                                'type': 'chapter'
                            })
                            
            elif book_name == "iching":
                for hexagram in book_data:
                    if isinstance(hexagram, dict):
                        name = hexagram.get('hexagram_name', '')
                        chinese = hexagram.get('hexagram_chinese', '')
                        meaning = hexagram.get('symbolic_meaning', '')
                        if name and meaning:
                            all_content.append({
                                'text': f"{name} {chinese} {meaning}",
                                'source': f"{name} ({chinese})",
                                'translation': meaning,
                                'book': book_name,
                                'type': 'hexagram'
                            })
                            
            elif book_name in ["positive_psy", "social_psy"]:
                if isinstance(book_data, dict):
                    for category_name, category_data in book_data.items():
                        if isinstance(category_data, dict) and 'concepts' in category_data:
                            for concept in category_data['concepts']:
                                if 'term' in concept and 'definition' in concept:
                                    all_content.append({
                                        'text': f"{concept['term']} {concept['definition']}",
                                        'source': concept['term'],
                                        'translation': concept['definition'],
                                        'book': book_name,
                                        'category': category_name,
                                        'type': 'concept'
                                    })
        
        print(f"📚 Extracted {len(all_content)} content pieces from all books")
        return all_content
    
    def build_embeddings(self, force_rebuild: bool = False):
        """Build or load embeddings for all content"""
        if not force_rebuild and self.content_cache_path.exists() and self.embeddings_cache_path.exists():
            # Load cached data
            with open(self.content_cache_path, 'rb') as f:
                self.content_data = pickle.load(f)
            with open(self.embeddings_cache_path, 'rb') as f:
                self.embeddings = pickle.load(f)
            print(f"📚 Loaded cached embeddings for {len(self.content_data)} documents")
            return
        
        # Extract content and create embeddings
        self.content_data = self.extract_all_content()
        
        if not self.content_data:
            print("❌ No content found")
            return
        
        print("🔨 Creating embeddings...")
        texts = [item['text'] for item in self.content_data]
        self.embeddings = self.model.encode(texts, show_progress_bar=True)
        
        # Cache the results
        with open(self.content_cache_path, 'wb') as f:
            pickle.dump(self.content_data, f)
        with open(self.embeddings_cache_path, 'wb') as f:
            pickle.dump(self.embeddings, f)
        
        print(f"✅ Built embeddings for {len(self.content_data)} documents")
    
    def search_relevant_content(self, query: str, top_k: int = 5, min_score: float = 0.3) -> List[Dict]:
        """Search for most relevant content"""
        if self.embeddings is None or not self.content_data:
            self.build_embeddings()
        
        if self.embeddings is None:
            return []
        
        # Create query embedding
        query_embedding = self.model.encode([query])
        
        # Calculate similarities
        similarities = util.cos_sim(query_embedding, self.embeddings)[0]
        
        # Get top results
        top_indices = similarities.topk(min(top_k, len(similarities))).indices.tolist()
        
        results = []
        for idx in top_indices:
            score = float(similarities[idx])
            if score >= min_score:
                result = self.content_data[idx].copy()
                result['relevance_score'] = score
                results.append(result)
        
        return results
    
    def get_statistics(self) -> Dict:
        """Get statistics about the content database"""
        if not self.content_data:
            self.build_embeddings()
        
        book_counts = {}
        for item in self.content_data:
            book = item['book']
            book_counts[book] = book_counts.get(book, 0) + 1
        
        return {
            "total_documents": len(self.content_data),
            "books": book_counts
        }

# Global instance
philosophy_rag = SimplePhilosophyRAG()
