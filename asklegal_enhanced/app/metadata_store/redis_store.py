import json
from typing import Dict, Any, List, Optional
import os
import pickle
from pathlib import Path

class RedisMetadataStore:
    """Simplified metadata store without Redis (uses local file storage)"""
    
    def __init__(self):
        # Use local file storage instead of Redis
        self.data_dir = Path("./data/metadata")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.client = {}  # In-memory storage
        print("Initialized simplified metadata store (file-based, no Redis required)")
    
    def store_document_metadata(self, doc_id: str, metadata: Dict[str, Any]) -> bool:
        """
        Store document metadata in local storage
        
        Args:
            doc_id (str): Document ID
            metadata (Dict[str, Any]): Document metadata
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Store in memory
            metadata_key = f"doc:{doc_id}:metadata"
            self.client[metadata_key] = json.dumps(metadata)
            
            # Also persist to disk
            file_path = self.data_dir / f"{doc_id}_metadata.json"
            with open(file_path, 'w') as f:
                json.dump(metadata, f)
            
            return True
        except Exception as e:
            print(f"Error storing document metadata: {e}")
            return False
    
    def get_document_metadata(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        Get document metadata from local storage
        
        Args:
            doc_id (str): Document ID
            
        Returns:
            Optional[Dict[str, Any]]: Document metadata or None if not found
        """
        try:
            # Try memory first
            metadata_key = f"doc:{doc_id}:metadata"
            if metadata_key in self.client:
                return json.loads(self.client[metadata_key])
            
            # Try disk
            file_path = self.data_dir / f"{doc_id}_metadata.json"
            if file_path.exists():
                with open(file_path, 'r') as f:
                    return json.load(f)
            
            return None
        except Exception as e:
            print(f"Error getting document metadata: {e}")
            return None
    
    def search_by_metadata(self, filters: Dict[str, Any], limit: int = 100) -> List[str]:
        """
        Search for documents by metadata filters (simplified)
        
        Args:
            filters (Dict[str, Any]): Metadata filters
            limit (int): Maximum number of results
            
        Returns:
            List[str]: Document IDs matching the filters
        """
        try:
            # Simple file-based search
            results = []
            for file_path in self.data_dir.glob("*_metadata.json"):
                doc_id = file_path.stem.replace("_metadata", "")
                results.append(doc_id)
                if len(results) >= limit:
                    break
            return results
        except Exception as e:
            print(f"Error searching by metadata: {e}")
            return []
    
    def store_clause_metadata(self, clause_id: str, doc_id: str, metadata: Dict[str, Any]) -> bool:
        """
        Store clause metadata (simplified)
        
        Args:
            clause_id (str): Clause ID
            doc_id (str): Document ID
            metadata (Dict[str, Any]): Clause metadata
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            clause_key = f"clause:{clause_id}:metadata"
            clause_data = {"doc_id": doc_id, **metadata}
            self.client[clause_key] = json.dumps(clause_data)
            return True
        except Exception as e:
            print(f"Error storing clause metadata: {e}")
            return False
    
    def get_document_clauses(self, doc_id: str) -> List[Dict[str, Any]]:
        """
        Get all clauses for a document (simplified)
        
        Args:
            doc_id (str): Document ID
            
        Returns:
            List[Dict[str, Any]]: List of clause metadata
        """
        # Simplified implementation
        return []

# Global instance
redis_store = RedisMetadataStore()