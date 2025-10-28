import redis
import json
from typing import Dict, Any, List, Optional
import os
from app.core.config import settings

class RedisMetadataStore:
    """Redis metadata store for fast metadata lookup"""
    
    def __init__(self):
        # Get Redis connection details
        self.host = os.getenv("REDIS_HOST", "localhost")
        self.port = int(os.getenv("REDIS_PORT", 6379))
        self.db = int(os.getenv("REDIS_DB", 0))
        
        try:
            # Connect to Redis
            self.client = redis.Redis(host=self.host, port=self.port, db=self.db, decode_responses=True)
            self.client.ping()
            print("Successfully connected to Redis")
        except Exception as e:
            print(f"Warning: Could not connect to Redis: {e}")
            self.client = None
    
    def store_document_metadata(self, doc_id: str, metadata: Dict[str, Any]) -> bool:
        """
        Store document metadata in Redis
        
        Args:
            doc_id (str): Document ID
            metadata (Dict[str, Any]): Document metadata
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.client:
            return False
            
        try:
            # Store metadata as JSON
            metadata_key = f"doc:{doc_id}:metadata"
            self.client.set(metadata_key, json.dumps(metadata))
            
            # Create indices for fast lookup
            self._create_indices(doc_id, metadata)
            
            return True
        except Exception as e:
            print(f"Error storing document metadata: {e}")
            return False
    
    def _create_indices(self, doc_id: str, metadata: Dict[str, Any]):
        """
        Create indices for fast metadata lookup
        
        Args:
            doc_id (str): Document ID
            metadata (Dict[str, Any]): Document metadata
        """
        if not self.client:
            return
            
        # Create indices for common metadata fields
        indexable_fields = ["document_type", "industry", "jurisdiction", "year", "author"]
        
        for field in indexable_fields:
            if field in metadata:
                value = metadata[field]
                index_key = f"index:{field}:{value}"
                self.client.sadd(index_key, doc_id)
    
    def get_document_metadata(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        Get document metadata from Redis
        
        Args:
            doc_id (str): Document ID
            
        Returns:
            Optional[Dict[str, Any]]: Document metadata or None if not found
        """
        if not self.client:
            return None
            
        try:
            metadata_key = f"doc:{doc_id}:metadata"
            metadata_json = self.client.get(metadata_key)
            
            if metadata_json:
                return json.loads(metadata_json)
            else:
                return None
        except Exception as e:
            print(f"Error getting document metadata: {e}")
            return None
    
    def search_by_metadata(self, filters: Dict[str, Any], limit: int = 100) -> List[str]:
        """
        Search for documents by metadata filters
        
        Args:
            filters (Dict[str, Any]): Metadata filters
            limit (int): Maximum number of results
            
        Returns:
            List[str]: Document IDs matching the filters
        """
        if not self.client:
            return []
            
        try:
            # Start with all documents or apply first filter
            if not filters:
                # Return all document IDs (simplified)
                keys = self.client.keys("doc:*:metadata")
                return [key.split(":")[1] for key in keys[:limit]]
            
            # Apply filters using set operations
            result_sets = []
            for field, value in filters.items():
                index_key = f"index:{field}:{value}"
                doc_ids = self.client.smembers(index_key)
                result_sets.append(set(doc_ids))
            
            # Intersect all result sets
            if result_sets:
                final_result = set.intersection(*result_sets)
                return list(final_result)[:limit]
            else:
                return []
                
        except Exception as e:
            print(f"Error searching by metadata: {e}")
            return []
    
    def store_clause_metadata(self, clause_id: str, doc_id: str, metadata: Dict[str, Any]) -> bool:
        """
        Store clause metadata in Redis
        
        Args:
            clause_id (str): Clause ID
            doc_id (str): Document ID
            metadata (Dict[str, Any]): Clause metadata
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.client:
            return False
            
        try:
            # Store clause metadata
            clause_key = f"clause:{clause_id}:metadata"
            clause_data = {"doc_id": doc_id, **metadata}
            self.client.set(clause_key, json.dumps(clause_data))
            
            # Add clause to document's clause list
            doc_clauses_key = f"doc:{doc_id}:clauses"
            self.client.sadd(doc_clauses_key, clause_id)
            
            return True
        except Exception as e:
            print(f"Error storing clause metadata: {e}")
            return False
    
    def get_document_clauses(self, doc_id: str) -> List[Dict[str, Any]]:
        """
        Get all clauses for a document
        
        Args:
            doc_id (str): Document ID
            
        Returns:
            List[Dict[str, Any]]: List of clause metadata
        """
        if not self.client:
            return []
            
        try:
            doc_clauses_key = f"doc:{doc_id}:clauses"
            clause_ids = self.client.smembers(doc_clauses_key)
            
            clauses = []
            for clause_id in clause_ids:
                clause_key = f"clause:{clause_id}:metadata"
                clause_json = self.client.get(clause_key)
                if clause_json:
                    clauses.append(json.loads(clause_json))
            
            return clauses
        except Exception as e:
            print(f"Error getting document clauses: {e}")
            return []

# Global instance
redis_store = RedisMetadataStore()