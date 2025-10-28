import numpy as np
from typing import List, Dict, Any, Tuple
from app.vector_store.faiss_store import faiss_store
from app.metadata_store.redis_store import redis_store
from app.document_processing.embedders import text_embedder
import re
from collections import Counter

class HybridRetriever:
    """Hybrid retrieval engine combining FAISS, Redis, and BM25"""
    
    def __init__(self):
        self.faiss_store = faiss_store
        self.redis_store = redis_store
        self.text_embedder = text_embedder
    
    def retrieve(self, query: str, limit: int = 10, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents using hybrid approach
        
        Args:
            query (str): Search query
            limit (int): Maximum number of results
            filters (Dict[str, Any], optional): Metadata filters
            
        Returns:
            List[Dict[str, Any]]: Retrieved documents with scores
        """
        # Get candidates from different sources
        faiss_results = self._retrieve_from_faiss(query, limit * 2)  # Get more candidates
        bm25_results = self._retrieve_with_bm25(query, limit * 2)
        metadata_results = self._retrieve_from_metadata(filters, limit * 2) if filters else []
        
        # Combine and re-rank results
        combined_results = self._combine_and_rerank(
            query, faiss_results, bm25_results, metadata_results, limit
        )
        
        return combined_results
    
    def _retrieve_from_faiss(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """Retrieve candidates using FAISS similarity search"""
        try:
            query_embedding = self.text_embedder.embed_text(query)
            results = self.faiss_store.search(query_embedding, limit)
            return results
        except Exception as e:
            print(f"FAISS retrieval failed: {e}")
            return []
    
    def _retrieve_with_bm25(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """Retrieve candidates using BM25 keyword matching"""
        # Simplified BM25 implementation
        query_terms = self._tokenize(query.lower())
        query_term_freq = Counter(query_terms)
        
        # Get all documents from FAISS as corpus (simplified)
        # In a real implementation, you would have a separate BM25 index
        try:
            # For demonstration, we'll simulate BM25 by keyword matching
            all_docs = []  # This would come from a BM25 index in practice
            
            # Simple keyword matching as BM25 approximation
            results = self.faiss_store.search(self.text_embedder.embed_text(""), 100)  # Get many docs
            
            scored_docs = []
            for doc in results:
                doc_terms = self._tokenize(doc["content"].lower())
                doc_term_freq = Counter(doc_terms)
                
                # Simple scoring based on term frequency
                score = 0
                for term, freq in query_term_freq.items():
                    if term in doc_term_freq:
                        score += freq * doc_term_freq[term]
                
                if score > 0:
                    doc["bm25_score"] = score
                    scored_docs.append(doc)
            
            # Sort by score and return top results
            scored_docs.sort(key=lambda x: x.get("bm25_score", 0), reverse=True)
            return scored_docs[:limit]
            
        except Exception as e:
            print(f"BM25 retrieval failed: {e}")
            return []
    
    def _retrieve_from_metadata(self, filters: Dict[str, Any], limit: int) -> List[Dict[str, Any]]:
        """Retrieve candidates using metadata filters"""
        if not self.redis_store:
            return []
            
        try:
            # Search by metadata filters
            doc_ids = self.redis_store.search_by_metadata(filters, limit)
            
            # Get document content from FAISS store
            results = []
            for doc_id in doc_ids:
                # This is a simplified approach - in practice, you'd map doc_ids to FAISS indices
                pass
                
            return results
        except Exception as e:
            print(f"Metadata retrieval failed: {e}")
            return []
    
    def _combine_and_rerank(self, query: str, faiss_results: List[Dict[str, Any]], 
                          bm25_results: List[Dict[str, Any]], metadata_results: List[Dict[str, Any]], 
                          limit: int) -> List[Dict[str, Any]]:
        """Combine and re-rank results from different sources"""
        # Create a unified result set
        all_results = {}
        
        # Add FAISS results (weight: 0.5)
        for result in faiss_results:
            doc_id = result["id"]
            if doc_id not in all_results:
                all_results[doc_id] = {"content": result["content"], "scores": {}}
            all_results[doc_id]["scores"]["faiss"] = result["score"] * 0.5
        
        # Add BM25 results (weight: 0.3)
        for result in bm25_results:
            doc_id = result["id"]
            if doc_id not in all_results:
                all_results[doc_id] = {"content": result["content"], "scores": {}}
            all_results[doc_id]["scores"]["bm25"] = result.get("bm25_score", 0) * 0.3
        
        # Add metadata results (weight: 0.2)
        for result in metadata_results:
            doc_id = result["id"]
            if doc_id not in all_results:
                all_results[doc_id] = {"content": result["content"], "scores": {}}
            all_results[doc_id]["scores"]["metadata"] = 0.2  # Fixed score for metadata match
        
        # Calculate combined scores
        combined_results = []
        for doc_id, data in all_results.items():
            # Weighted sum of scores
            combined_score = sum(data["scores"].values())
            
            combined_results.append({
                "id": doc_id,
                "content": data["content"],
                "score": combined_score,
                "scores": data["scores"]
            })
        
        # Sort by combined score
        combined_results.sort(key=lambda x: x["score"], reverse=True)
        
        return combined_results[:limit]
    
    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenizer for BM25"""
        # Remove punctuation and split by whitespace
        tokens = re.findall(r'\b\w+\b', text)
        return [token for token in tokens if len(token) > 2]  # Filter short tokens

# Global instance
hybrid_retriever = HybridRetriever()