"""
Upstash Redis Manager for Chat History and Caching
"""

import logging
import json
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from upstash_redis import Redis
from app.core.config_enhanced import settings

logger = logging.getLogger(__name__)

class UpstashRedisManager:
    """
    Manages Upstash Redis for:
    - Chat history persistence
    - Query caching
    - Session management
    - Metadata storage
    """
    
    def __init__(self):
        self.client: Optional[Redis] = None
        self._connect()
        
    def _connect(self):
        """Connect to Upstash Redis"""
        try:
            if settings.UPSTASH_REDIS_URL and settings.UPSTASH_REDIS_TOKEN:
                self.client = Redis(
                    url=settings.UPSTASH_REDIS_URL,
                    token=settings.UPSTASH_REDIS_TOKEN
                )
                # Test connection
                self.client.ping()
                logger.info("✓ Connected to Upstash Redis successfully")
            else:
                logger.warning("Upstash Redis credentials not provided")
                logger.info("Chat history will not persist across sessions")
        except Exception as e:
            logger.error(f"Failed to connect to Upstash Redis: {e}")
            self.client = None
    
    def is_connected(self) -> bool:
        """Check if Redis is connected"""
        return self.client is not None
    
    # Chat History Management
    
    def save_message(
        self,
        session_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Save a chat message to history"""
        if not self.client:
            return False
            
        try:
            message = {
                "role": role,
                "content": content,
                "timestamp": datetime.now().isoformat(),
                "metadata": metadata or {}
            }
            
            key = f"chat:{session_id}"
            self.client.rpush(key, json.dumps(message))
            
            # Set expiry for 30 days
            self.client.expire(key, 30 * 24 * 60 * 60)
            
            return True
        except Exception as e:
            logger.error(f"Failed to save message: {e}")
            return False
    
    def get_chat_history(
        self,
        session_id: str,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve chat history for a session"""
        if not self.client:
            return []
            
        try:
            key = f"chat:{session_id}"
            
            if limit:
                messages = self.client.lrange(key, -limit, -1)
            else:
                messages = self.client.lrange(key, 0, -1)
            
            return [json.loads(msg) for msg in messages]
        except Exception as e:
            logger.error(f"Failed to get chat history: {e}")
            return []
    
    def clear_chat_history(self, session_id: str) -> bool:
        """Clear chat history for a session"""
        if not self.client:
            return False
            
        try:
            key = f"chat:{session_id}"
            self.client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Failed to clear chat history: {e}")
            return False
    
    # Query Caching
    
    def cache_query_result(
        self,
        query_hash: str,
        result: Any,
        ttl: int = 3600
    ) -> bool:
        """Cache a query result"""
        if not self.client:
            return False
            
        try:
            key = f"cache:query:{query_hash}"
            self.client.setex(key, ttl, json.dumps(result))
            return True
        except Exception as e:
            logger.error(f"Failed to cache query result: {e}")
            return False
    
    def get_cached_query_result(self, query_hash: str) -> Optional[Any]:
        """Retrieve cached query result"""
        if not self.client:
            return None
            
        try:
            key = f"cache:query:{query_hash}"
            result = self.client.get(key)
            return json.loads(result) if result else None
        except Exception as e:
            logger.error(f"Failed to get cached result: {e}")
            return None
    
    # Document Metadata Storage
    
    def save_document_metadata(
        self,
        doc_id: str,
        metadata: Dict[str, Any]
    ) -> bool:
        """Save document metadata"""
        if not self.client:
            return False
            
        try:
            key = f"doc:metadata:{doc_id}"
            self.client.set(key, json.dumps(metadata))
            return True
        except Exception as e:
            logger.error(f"Failed to save document metadata: {e}")
            return False
    
    def get_document_metadata(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve document metadata"""
        if not self.client:
            return None
            
        try:
            key = f"doc:metadata:{doc_id}"
            result = self.client.get(key)
            return json.loads(result) if result else None
        except Exception as e:
            logger.error(f"Failed to get document metadata: {e}")
            return None
    
    def list_user_documents(self, user_id: str) -> List[str]:
        """List all documents for a user"""
        if not self.client:
            return []
            
        try:
            key = f"user:docs:{user_id}"
            return self.client.smembers(key) or []
        except Exception as e:
            logger.error(f"Failed to list user documents: {e}")
            return []
    
    def add_user_document(self, user_id: str, doc_id: str) -> bool:
        """Add document to user's list"""
        if not self.client:
            return False
            
        try:
            key = f"user:docs:{user_id}"
            self.client.sadd(key, doc_id)
            return True
        except Exception as e:
            logger.error(f"Failed to add user document: {e}")
            return False
    
    # Session Management
    
    def create_session(
        self,
        session_id: str,
        user_id: Optional[str] = None,
        ttl: int = 24 * 60 * 60
    ) -> bool:
        """Create a new session"""
        if not self.client:
            return False
            
        try:
            session_data = {
                "session_id": session_id,
                "user_id": user_id,
                "created_at": datetime.now().isoformat(),
                "last_activity": datetime.now().isoformat()
            }
            
            key = f"session:{session_id}"
            self.client.setex(key, ttl, json.dumps(session_data))
            return True
        except Exception as e:
            logger.error(f"Failed to create session: {e}")
            return False
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve session data"""
        if not self.client:
            return None
            
        try:
            key = f"session:{session_id}"
            result = self.client.get(key)
            return json.loads(result) if result else None
        except Exception as e:
            logger.error(f"Failed to get session: {e}")
            return None
    
    def update_session_activity(self, session_id: str) -> bool:
        """Update session last activity timestamp"""
        if not self.client:
            return False
            
        try:
            session = self.get_session(session_id)
            if session:
                session["last_activity"] = datetime.now().isoformat()
                key = f"session:{session_id}"
                self.client.set(key, json.dumps(session))
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to update session activity: {e}")
            return False
    
    # Statistics and Monitoring
    
    def increment_query_count(self, date: Optional[str] = None) -> bool:
        """Increment daily query count"""
        if not self.client:
            return False
            
        try:
            date = date or datetime.now().strftime("%Y-%m-%d")
            key = f"stats:queries:{date}"
            self.client.incr(key)
            self.client.expire(key, 90 * 24 * 60 * 60)  # Keep for 90 days
            return True
        except Exception as e:
            logger.error(f"Failed to increment query count: {e}")
            return False
    
    def get_query_count(self, date: Optional[str] = None) -> int:
        """Get query count for a date"""
        if not self.client:
            return 0
            
        try:
            date = date or datetime.now().strftime("%Y-%m-%d")
            key = f"stats:queries:{date}"
            count = self.client.get(key)
            return int(count) if count else 0
        except Exception as e:
            logger.error(f"Failed to get query count: {e}")
            return 0

# Global instance
redis_manager = None

def get_redis_manager() -> UpstashRedisManager:
    """Get or create Redis manager singleton"""
    global redis_manager
    if redis_manager is None:
        redis_manager = UpstashRedisManager()
    return redis_manager
