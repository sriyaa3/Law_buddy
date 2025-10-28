from neo4j import GraphDatabase
from typing import List, Dict, Any
import os
from app.core.config import settings

class Neo4jConnector:
    """Neo4j graph database connector for legal knowledge graph"""
    
    def __init__(self):
        # Get connection details from environment or settings
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.username = os.getenv("NEO4J_USERNAME", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD", "password")
        
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))
            self._verify_connection()
        except Exception as e:
            print(f"Warning: Could not connect to Neo4j database: {e}")
            self.driver = None
    
    def _verify_connection(self):
        """Verify connection to Neo4j database"""
        if not self.driver:
            return False
            
        try:
            with self.driver.session() as session:
                session.run("RETURN 1")
            print("Successfully connected to Neo4j database")
            return True
        except Exception as e:
            print(f"Failed to connect to Neo4j database: {e}")
            return False
    
    def close(self):
        """Close the database connection"""
        if self.driver:
            self.driver.close()
    
    def create_document_node(self, doc_id: str, metadata: Dict[str, Any]) -> bool:
        """
        Create a document node in the graph
        
        Args:
            doc_id (str): Document ID
            metadata (Dict[str, Any]): Document metadata
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.driver:
            return False
            
        try:
            with self.driver.session() as session:
                query = """
                MERGE (d:Document {id: $doc_id})
                SET d += $metadata
                RETURN d
                """
                session.run(query, doc_id=doc_id, metadata=metadata)
            return True
        except Exception as e:
            print(f"Error creating document node: {e}")
            return False
    
    def create_clause_node(self, clause_id: str, text: str, doc_id: str, metadata: Dict[str, Any] = None) -> bool:
        """
        Create a clause node in the graph
        
        Args:
            clause_id (str): Clause ID
            text (str): Clause text
            doc_id (str): Document ID
            metadata (Dict[str, Any], optional): Additional metadata
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.driver:
            return False
            
        try:
            with self.driver.session() as session:
                query = """
                MERGE (c:Clause {id: $clause_id})
                SET c.text = $text
                SET c += $metadata
                WITH c
                MATCH (d:Document {id: $doc_id})
                MERGE (d)-[:CONTAINS]->(c)
                RETURN c
                """
                session.run(query, clause_id=clause_id, text=text, doc_id=doc_id, metadata=metadata or {})
            return True
        except Exception as e:
            print(f"Error creating clause node: {e}")
            return False
    
    def create_entity_node(self, entity_id: str, text: str, label: str, metadata: Dict[str, Any] = None) -> bool:
        """
        Create an entity node in the graph
        
        Args:
            entity_id (str): Entity ID
            text (str): Entity text
            label (str): Entity label/type
            metadata (Dict[str, Any], optional): Additional metadata
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.driver:
            return False
            
        try:
            with self.driver.session() as session:
                query = """
                MERGE (e:Entity {id: $entity_id})
                SET e.text = $text, e.label = $label
                SET e += $metadata
                RETURN e
                """
                session.run(query, entity_id=entity_id, text=text, label=label, metadata=metadata or {})
            return True
        except Exception as e:
            print(f"Error creating entity node: {e}")
            return False
    
    def create_relationship(self, from_id: str, to_id: str, relationship_type: str, properties: Dict[str, Any] = None) -> bool:
        """
        Create a relationship between two nodes
        
        Args:
            from_id (str): Source node ID
            to_id (str): Target node ID
            relationship_type (str): Type of relationship
            properties (Dict[str, Any], optional): Relationship properties
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.driver:
            return False
            
        try:
            with self.driver.session() as session:
                query = f"""
                MATCH (a {{id: $from_id}}), (b {{id: $to_id}})
                MERGE (a)-[r:{relationship_type}]->(b)
                SET r += $properties
                RETURN r
                """
                session.run(query, from_id=from_id, to_id=to_id, properties=properties or {})
            return True
        except Exception as e:
            print(f"Error creating relationship: {e}")
            return False
    
    def search_clauses(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for clauses using text similarity
        
        Args:
            query (str): Search query
            limit (int): Maximum number of results
            
        Returns:
            List[Dict[str, Any]]: Matching clauses
        """
        if not self.driver:
            return []
            
        try:
            with self.driver.session() as session:
                cypher_query = """
                MATCH (c:Clause)
                WHERE toLower(c.text) CONTAINS toLower($query)
                RETURN c.id AS id, c.text AS text, c.document_id AS document_id
                LIMIT $limit
                """
                result = session.run(cypher_query, query=query, limit=limit)
                return [record.data() for record in result]
        except Exception as e:
            print(f"Error searching clauses: {e}")
            return []
    
    def get_document_structure(self, doc_id: str) -> Dict[str, Any]:
        """
        Get the structure of a document (clauses and entities)
        
        Args:
            doc_id (str): Document ID
            
        Returns:
            Dict[str, Any]: Document structure
        """
        if not self.driver:
            return {}
            
        try:
            with self.driver.session() as session:
                # Get clauses
                clause_query = """
                MATCH (d:Document {id: $doc_id})-[:CONTAINS]->(c:Clause)
                RETURN c.id AS id, c.text AS text
                ORDER BY c.id
                """
                clauses_result = session.run(clause_query, doc_id=doc_id)
                clauses = [record.data() for record in clauses_result]
                
                # Get entities
                entity_query = """
                MATCH (d:Document {id: $doc_id})-[:CONTAINS]->(c:Clause)-[:MENTIONS]->(e:Entity)
                RETURN DISTINCT e.id AS id, e.text AS text, e.label AS label
                """
                entities_result = session.run(entity_query, doc_id=doc_id)
                entities = [record.data() for record in entities_result]
                
                return {
                    "clauses": clauses,
                    "entities": entities
                }
        except Exception as e:
            print(f"Error getting document structure: {e}")
            return {}

# Global instance
neo4j_connector = Neo4jConnector()