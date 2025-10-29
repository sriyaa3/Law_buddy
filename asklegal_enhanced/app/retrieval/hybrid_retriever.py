"""
Simple hybrid retriever for AskLegal Enhanced
Combines vector similarity search with keyword matching
"""
import os
from pathlib import Path
from typing import List, Dict, Optional
import numpy as np

class HybridRetriever:
    """Hybrid retrieval system combining FAISS and keyword search"""
    
    def __init__(self):
        self.index = None
        self.documents = []
        self.metadata = {}
        self._initialize()
    
    def _initialize(self):
        """Initialize the retriever with existing index"""
        try:
            import faiss
            index_path = Path("./data/legal_documents.index")
            
            if index_path.exists():
                self.index = faiss.read_index(str(index_path))
                
                # Load metadata if available
                import json
                metadata_path = Path("./data/legal_documents_metadata.json")
                if metadata_path.exists():
                    with open(metadata_path, 'r') as f:
                        self.metadata = json.load(f)
                        self.documents = self.metadata.get('chunks', [])
        except Exception as e:
            print(f"Warning: Could not initialize retriever: {e}")
    
    def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Retrieve relevant documents for a query
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of relevant document chunks with scores
        """
        results = []
        
        # If we have a valid index, use it
        if self.index and self.index.ntotal > 0:
            try:
                from sentence_transformers import SentenceTransformer
                
                # Get query embedding
                model = SentenceTransformer('all-MiniLM-L6-v2', cache_folder='./models/embeddings')
                query_embedding = model.encode([query])[0].reshape(1, -1).astype('float32')
                
                # Search
                distances, indices = self.index.search(query_embedding, min(top_k, self.index.ntotal))
                
                # Format results
                for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
                    if idx < len(self.documents):
                        results.append({
                            'text': self.documents[idx],
                            'score': float(1 / (1 + dist)),  # Convert distance to similarity score
                            'rank': i + 1
                        })
            except Exception as e:
                print(f"Vector search failed: {e}")
        
        # If no results from vector search, do simple keyword matching
        if not results and self.documents:
            query_lower = query.lower()
            for doc in self.documents[:top_k]:
                if any(word in doc.lower() for word in query_lower.split()):
                    results.append({
                        'text': doc,
                        'score': 0.5,
                        'rank': len(results) + 1
                    })
        
        # Fallback: return generic legal response context
        if not results:
            results = [{
                'text': 'Indian legal system information available. Please ask specific questions about IPC, CPC, CrPC, or other legal acts.',
                'score': 0.3,
                'rank': 1
            }]
        
        return results[:top_k]
    
    def get_context(self, query: str, max_length: int = 1000) -> str:
        """
        Get concatenated context for a query
        
        Args:
            query: Search query
            max_length: Maximum context length
            
        Returns:
            Concatenated context string
        """
        results = self.retrieve(query)
        
        context_parts = []
        current_length = 0
        
        for result in results:
            text = result['text']
            if current_length + len(text) <= max_length:
                context_parts.append(text)
                current_length += len(text)
            else:
                break
        
        return "\n\n".join(context_parts)

# Global instance
hybrid_retriever = HybridRetriever()
