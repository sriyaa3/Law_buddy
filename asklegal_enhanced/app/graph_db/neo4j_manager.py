"""
Neo4j Clause-Graph Manager
Manages legal clause relationships and knowledge graph
"""

import logging
from typing import List, Dict, Any, Optional
from neo4j import GraphDatabase, Driver
from app.core.config_enhanced import settings

logger = logging.getLogger(__name__)

class Neo4jClauseGraphManager:
    """
    Manages clause-graph construction and querying in Neo4j
    Represents legal documents as graphs with:
    - Clauses as nodes
    - Relationships between clauses
    - Entity extraction and linking
    """
    
    def __init__(self):
        self.driver: Optional[Driver] = None
        self._connect()
        
    def _connect(self):
        """Establish connection to Neo4j"""
        try:
            self.driver = GraphDatabase.driver(
                settings.NEO4J_URI,
                auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
            )
            # Test connection
            with self.driver.session() as session:
                session.run("RETURN 1")
            logger.info("✓ Connected to Neo4j successfully")
            self._create_indexes()
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            logger.warning("Neo4j clause-graph features will be unavailable")
            self.driver = None
    
    def _create_indexes(self):
        """Create necessary indexes for performance"""
        if not self.driver:
            return
            
        indexes = [
            "CREATE INDEX clause_id IF NOT EXISTS FOR (c:Clause) ON (c.id)",
            "CREATE INDEX entity_name IF NOT EXISTS FOR (e:Entity) ON (e.name)",
            "CREATE INDEX document_id IF NOT EXISTS FOR (d:Document) ON (d.id)",
        ]
        
        try:
            with self.driver.session() as session:
                for index_query in indexes:
                    session.run(index_query)
            logger.info("✓ Neo4j indexes created")
        except Exception as e:
            logger.warning(f"Failed to create indexes: {e}")
    
    def close(self):
        """Close Neo4j connection"""
        if self.driver:
            self.driver.close()
            logger.info("Neo4j connection closed")
    
    def create_document_node(self, doc_id: str, metadata: Dict[str, Any]) -> bool:
        """Create a document node"""
        if not self.driver:
            return False
            
        query = """
        MERGE (d:Document {id: $doc_id})
        SET d += $metadata
        RETURN d
        """
        
        try:
            with self.driver.session() as session:
                session.run(query, doc_id=doc_id, metadata=metadata)
            return True
        except Exception as e:
            logger.error(f"Failed to create document node: {e}")
            return False
    
    def create_clause_node(
        self,
        clause_id: str,
        doc_id: str,
        text: str,
        clause_type: str,
        position: int,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Create a clause node and link to document"""
        if not self.driver:
            return False
            
        query = """
        MATCH (d:Document {id: $doc_id})
        MERGE (c:Clause {id: $clause_id})
        SET c.text = $text,
            c.type = $clause_type,
            c.position = $position
        SET c += $metadata
        MERGE (d)-[:CONTAINS]->(c)
        RETURN c
        """
        
        try:
            with self.driver.session() as session:
                session.run(
                    query,
                    clause_id=clause_id,
                    doc_id=doc_id,
                    text=text,
                    clause_type=clause_type,
                    position=position,
                    metadata=metadata or {}
                )
            return True
        except Exception as e:
            logger.error(f"Failed to create clause node: {e}")
            return False
    
    def create_entity_node(
        self,
        entity_name: str,
        entity_type: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Create an entity node"""
        if not self.driver:
            return False
            
        query = """
        MERGE (e:Entity {name: $entity_name})
        SET e.type = $entity_type
        SET e += $metadata
        RETURN e
        """
        
        try:
            with self.driver.session() as session:
                session.run(
                    query,
                    entity_name=entity_name,
                    entity_type=entity_type,
                    metadata=metadata or {}
                )
            return True
        except Exception as e:
            logger.error(f"Failed to create entity node: {e}")
            return False
    
    def link_clause_to_entity(self, clause_id: str, entity_name: str) -> bool:
        """Create relationship between clause and entity"""
        if not self.driver:
            return False
            
        query = """
        MATCH (c:Clause {id: $clause_id})
        MATCH (e:Entity {name: $entity_name})
        MERGE (c)-[:MENTIONS]->(e)
        """
        
        try:
            with self.driver.session() as session:
                session.run(query, clause_id=clause_id, entity_name=entity_name)
            return True
        except Exception as e:
            logger.error(f"Failed to link clause to entity: {e}")
            return False
    
    def create_clause_relationship(
        self,
        from_clause_id: str,
        to_clause_id: str,
        relationship_type: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Create relationship between clauses"""
        if not self.driver:
            return False
            
        query = f"""
        MATCH (c1:Clause {{id: $from_clause_id}})
        MATCH (c2:Clause {{id: $to_clause_id}})
        MERGE (c1)-[r:{relationship_type}]->(c2)
        SET r += $properties
        """
        
        try:
            with self.driver.session() as session:
                session.run(
                    query,
                    from_clause_id=from_clause_id,
                    to_clause_id=to_clause_id,
                    properties=properties or {}
                )
            return True
        except Exception as e:
            logger.error(f"Failed to create clause relationship: {e}")
            return False
    
    def find_related_clauses(
        self,
        clause_id: str,
        relationship_types: Optional[List[str]] = None,
        max_depth: int = 2
    ) -> List[Dict[str, Any]]:
        """Find related clauses through graph traversal"""
        if not self.driver:
            return []
            
        rel_filter = ""
        if relationship_types:
            rel_types = "|".join(relationship_types)
            rel_filter = f":{rel_types}"
            
        query = f"""
        MATCH path = (c1:Clause {{id: $clause_id}})-[r{rel_filter}*1..{max_depth}]-(c2:Clause)
        RETURN DISTINCT c2.id as id, c2.text as text, c2.type as type, length(path) as distance
        ORDER BY distance
        """
        
        try:
            with self.driver.session() as session:
                result = session.run(query, clause_id=clause_id)
                return [dict(record) for record in result]
        except Exception as e:
            logger.error(f"Failed to find related clauses: {e}")
            return []
    
    def find_clauses_by_entity(self, entity_name: str) -> List[Dict[str, Any]]:
        """Find all clauses mentioning a specific entity"""
        if not self.driver:
            return []
            
        query = """
        MATCH (c:Clause)-[:MENTIONS]->(e:Entity {name: $entity_name})
        RETURN c.id as id, c.text as text, c.type as type
        """
        
        try:
            with self.driver.session() as session:
                result = session.run(query, entity_name=entity_name)
                return [dict(record) for record in result]
        except Exception as e:
            logger.error(f"Failed to find clauses by entity: {e}")
            return []
    
    def get_document_structure(self, doc_id: str) -> Dict[str, Any]:
        """Get complete structure of a document"""
        if not self.driver:
            return {}
            
        query = """
        MATCH (d:Document {id: $doc_id})-[:CONTAINS]->(c:Clause)
        OPTIONAL MATCH (c)-[:MENTIONS]->(e:Entity)
        RETURN d, 
               collect(DISTINCT {
                   id: c.id, 
                   text: c.text, 
                   type: c.type,
                   position: c.position
               }) as clauses,
               collect(DISTINCT e.name) as entities
        """
        
        try:
            with self.driver.session() as session:
                result = session.run(query, doc_id=doc_id)
                record = result.single()
                if record:
                    return {
                        "document": dict(record["d"]),
                        "clauses": record["clauses"],
                        "entities": [e for e in record["entities"] if e is not None]
                    }
        except Exception as e:
            logger.error(f"Failed to get document structure: {e}")
        
        return {}
    
    def search_clauses_by_text(self, search_text: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search clauses by text content"""
        if not self.driver:
            return []
            
        query = """
        MATCH (c:Clause)
        WHERE toLower(c.text) CONTAINS toLower($search_text)
        RETURN c.id as id, c.text as text, c.type as type
        LIMIT $limit
        """
        
        try:
            with self.driver.session() as session:
                result = session.run(query, search_text=search_text, limit=limit)
                return [dict(record) for record in result]
        except Exception as e:
            logger.error(f"Failed to search clauses: {e}")
            return []
    
    def delete_document(self, doc_id: str) -> bool:
        """Delete a document and all its clauses"""
        if not self.driver:
            return False
            
        query = """
        MATCH (d:Document {id: $doc_id})
        OPTIONAL MATCH (d)-[:CONTAINS]->(c:Clause)
        DETACH DELETE c, d
        """
        
        try:
            with self.driver.session() as session:
                session.run(query, doc_id=doc_id)
            return True
        except Exception as e:
            logger.error(f"Failed to delete document: {e}")
            return False

# Global instance
clause_graph_manager = None

def get_clause_graph_manager() -> Neo4jClauseGraphManager:
    """Get or create clause graph manager singleton"""
    global clause_graph_manager
    if clause_graph_manager is None:
        clause_graph_manager = Neo4jClauseGraphManager()
    return clause_graph_manager
