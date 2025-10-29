from typing import List, Dict, Any
import numpy as np
import pickle
import os
from app.core.config import settings

class FAISSVectorStore:
    """Simplified vector store without FAISS dependency"""
    
    def __init__(self, index_name: str = "legal_documents", vector_size: int = 384):
        """
        Initialize the simplified vector store
        
        Args:
            index_name (str): Name of the index to use
            vector_size (int): Size of the vectors
        """
        self.index_name = index_name
        self.vector_size = vector_size
        
        # Create data directory if it doesn't exist
        data_dir = "./data"
        os.makedirs(data_dir, exist_ok=True)
        
        self.metadata_file = os.path.join(data_dir, f"{index_name}_metadata.pkl")
        self.vectors_file = os.path.join(data_dir, f"{index_name}_vectors.pkl")
        
        # Initialize storage
        self.vectors = []
        self.metadata = []
        
        # Load existing data if it exists
        self._load_index()
        print(f"Initialized simplified vector store with {len(self.metadata)} documents")
    
    def _load_index(self):
        """Load the index from disk if it exists"""
        if os.path.exists(self.metadata_file) and os.path.exists(self.vectors_file):
            try:
                with open(self.metadata_file, 'rb') as f:
                    self.metadata = pickle.load(f)
                with open(self.vectors_file, 'rb') as f:
                    self.vectors = pickle.load(f)
                print(f"Loaded vector store with {len(self.metadata)} vectors")
            except Exception as e:
                print(f"Error loading vector store: {e}")
                self.vectors = []
                self.metadata = []
        else:
            print("Creating new vector store")
    
    def _save_index(self):
        """Save the index to disk"""
        try:
            with open(self.metadata_file, 'wb') as f:
                pickle.dump(self.metadata, f)
            with open(self.vectors_file, 'wb') as f:
                pickle.dump(self.vectors, f)
            print(f"Saved vector store with {len(self.metadata)} vectors")
        except Exception as e:
            print(f"Error saving vector store: {e}")
    
    def normalize_vectors(self, vectors: np.ndarray) -> np.ndarray:
        """Normalize vectors for cosine similarity"""
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        return vectors / (norms + 1e-8)
    
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
        
        # Add vectors and metadata
        for i, (document, embedding) in enumerate(zip(documents, normalized_embeddings)):
            self.vectors.append(embedding)
            self.metadata.append({
                "content": document.get("text", ""),
                "metadata": document.get("metadata", {}),
                "type": document.get("type", "unknown")
            })
        
        # Save index
        self._save_index()
        
        # Return document IDs
        doc_ids = [str(i) for i in range(len(self.metadata) - len(documents), len(self.metadata))]
        return doc_ids
    
    def search(self, query_embedding: np.ndarray, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar documents using cosine similarity
        
        Args:
            query_embedding (np.ndarray): Query embedding
            limit (int): Number of results to return
            
        Returns:
            List[Dict[str, Any]]: List of similar documents
        """
        if len(self.vectors) == 0:
            return []
        
        try:
            # Normalize query embedding
            query_norm = query_embedding / (np.linalg.norm(query_embedding) + 1e-8)
            
            # Calculate cosine similarity with all vectors
            similarities = []
            for idx, vec in enumerate(self.vectors):
                similarity = np.dot(query_norm, vec)
                similarities.append((similarity, idx))
            
            # Sort by similarity
            similarities.sort(reverse=True, key=lambda x: x[0])
            
            # Format results
            results = []
            for score, idx in similarities[:limit]:
                if idx < len(self.metadata):
                    results.append({
                        "id": str(idx),
                        "score": float(score),
                        "content": self.metadata[idx]["content"],
                        "metadata": self.metadata[idx]["metadata"],
                        "type": self.metadata[idx]["type"]
                    })
            
            return results
        except Exception as e:
            print(f"Vector search failed: {e}")
            return []
    
    def delete_index(self):
        """Delete the index files"""
        try:
            if os.path.exists(self.metadata_file):
                os.remove(self.metadata_file)
            if os.path.exists(self.vectors_file):
                os.remove(self.vectors_file)
            self.vectors = []
            self.metadata = []
            print(f"Deleted vector store: {self.index_name}")
        except Exception as e:
            print(f"Error deleting vector store: {e}")

# Global instance
faiss_store = FAISSVectorStore()