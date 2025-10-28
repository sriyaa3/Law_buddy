from typing import List, Dict, Any
import numpy as np
import faiss
import pickle
import os
from app.core.config import settings

class FAISSVectorStore:
    """Vector store implementation using FAISS"""
    
    def __init__(self, index_name: str = "legal_documents", vector_size: int = 384):
        """
        Initialize the FAISS vector store
        
        Args:
            index_name (str): Name of the index to use
            vector_size (int): Size of the vectors
        """
        self.index_name = index_name
        self.vector_size = vector_size
        
        # Create data directory if it doesn't exist
        data_dir = "./data"
        os.makedirs(data_dir, exist_ok=True)
        
        self.index_file = os.path.join(data_dir, f"{index_name}.index")
        self.metadata_file = os.path.join(data_dir, f"{index_name}_metadata.pkl")
        
        # Initialize FAISS index
        self.index = faiss.IndexFlatIP(vector_size)  # Inner product for cosine similarity
        self.metadata = []
        
        # Load existing index if it exists
        self._load_index()
    
    def _load_index(self):
        """Load the index from disk if it exists"""
        if os.path.exists(self.index_file) and os.path.exists(self.metadata_file):
            try:
                self.index = faiss.read_index(self.index_file)
                with open(self.metadata_file, 'rb') as f:
                    self.metadata = pickle.load(f)
                print(f"Loaded FAISS index with {self.index.ntotal} vectors")
            except Exception as e:
                print(f"Error loading FAISS index: {e}")
                # Reset to empty index
                self.index = faiss.IndexFlatIP(self.vector_size)
                self.metadata = []
        else:
            print("Creating new FAISS index")
    
    def _save_index(self):
        """Save the index to disk"""
        try:
            faiss.write_index(self.index, self.index_file)
            with open(self.metadata_file, 'wb') as f:
                pickle.dump(self.metadata, f)
            print(f"Saved FAISS index with {self.index.ntotal} vectors")
        except Exception as e:
            print(f"Error saving FAISS index: {e}")
    
    def normalize_vectors(self, vectors: np.ndarray) -> np.ndarray:
        """Normalize vectors for cosine similarity"""
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        return vectors / (norms + 1e-8)  # Add small epsilon to avoid division by zero
    
    def add_documents(self, documents: List[Dict[str, Any]], embeddings: np.ndarray) -> List[str]:
        """
        Add documents to the vector store
        
        Args:
            documents (List[Dict[str, Any]]): List of document data
            embeddings (np.ndarray): Document embeddings
            
        Returns:
            List[str]: List of document IDs
        """
        if len(documents) != len(embeddings):
            raise ValueError("Number of documents must match number of embeddings")
        
        # Normalize embeddings for cosine similarity
        normalized_embeddings = self.normalize_vectors(embeddings)
        
        # Add vectors to index
        self.index.add(normalized_embeddings.astype(np.float32))
        
        # Store metadata
        for document in documents:
            self.metadata.append({
                "content": document.get("text", ""),
                "metadata": document.get("metadata", {}),
                "type": document.get("type", "unknown")
            })
        
        # Save index
        self._save_index()
        
        # Return document IDs (indices in our case)
        doc_ids = [str(i) for i in range(len(self.metadata) - len(documents), len(self.metadata))]
        return doc_ids
    
    def search(self, query_embedding: np.ndarray, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar documents
        
        Args:
            query_embedding (np.ndarray): Query embedding
            limit (int): Number of results to return
            
        Returns:
            List[Dict[str, Any]]: List of similar documents
        """
        if self.index.ntotal == 0:
            return []
        
        try:
            # Normalize query embedding
            normalized_query = self.normalize_vectors(query_embedding.reshape(1, -1))
            
            # Perform search
            scores, indices = self.index.search(normalized_query.astype(np.float32), min(limit, self.index.ntotal))
            
            # Format results
            results = []
            for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                if idx < len(self.metadata) and idx >= 0:
                    results.append({
                        "id": str(idx),
                        "score": float(score),
                        "content": self.metadata[idx]["content"],
                        "metadata": self.metadata[idx]["metadata"],
                        "type": self.metadata[idx]["type"]
                    })
            
            return results
        except Exception as e:
            print(f"FAISS search failed: {e}")
            return []
    
    def delete_index(self):
        """Delete the index files"""
        try:
            if os.path.exists(self.index_file):
                os.remove(self.index_file)
            if os.path.exists(self.metadata_file):
                os.remove(self.metadata_file)
            self.index = faiss.IndexFlatIP(self.vector_size)
            self.metadata = []
            print(f"Deleted FAISS index: {self.index_name}")
        except Exception as e:
            print(f"Error deleting FAISS index: {e}")

# Global instance
faiss_store = FAISSVectorStore()