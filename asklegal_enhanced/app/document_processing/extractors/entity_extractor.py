import spacy
from typing import List, Dict, Any
import re

class LegalEntityExtractor:
    """Legal entity extractor using spaCy and rule-based patterns"""
    
    def __init__(self):
        # Load spaCy model (this would need to be downloaded separately)
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Warning: spaCy model not found. Please install with: python -m spacy download en_core_web_sm")
            self.nlp = None
    
    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract legal entities from text
        
        Args:
            text (str): Text to analyze
            
        Returns:
            List[Dict[str, Any]]: Extracted entities
        """
        entities = []
        
        # Rule-based extraction for legal-specific entities
        legal_entities = self._extract_legal_entities(text)
        entities.extend(legal_entities)
        
        # spaCy NER if available
        if self.nlp:
            try:
                doc = self.nlp(text)
                for ent in doc.ents:
                    entities.append({
                        "text": ent.text,
                        "label": ent.label_,
                        "start": ent.start_char,
                        "end": ent.end_char,
                        "description": self._get_entity_description(ent.label_)
                    })
            except Exception as e:
                print(f"spaCy NER failed: {e}")
        
        return entities
    
    def _extract_legal_entities(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract legal entities using rule-based patterns
        
        Args:
            text (str): Text to analyze
            
        Returns:
            List[Dict[str, Any]]: Extracted legal entities
        """
        entities = []
        
        # Legal entity patterns
        patterns = {
            "SECTION": [
                r"Section\s+(\d+[A-Za-z]*)",
                r"Sec\.\s*(\d+[A-Za-z]*)",
                r"S\.\s*(\d+[A-Za-z]*)"
            ],
            "ACT": [
                r"([A-Z][A-Za-z\s]+Act),?\s+(\d+)",
                r"the\s+([A-Z][A-Za-z\s]+) Act"
            ],
            "COURT": [
                r"Supreme Court",
                r"High Court",
                r"([A-Z][A-Za-z\s]+) High Court"
            ],
            "CASE": [
                r"([A-Z][A-Za-z\s]+) v\.? ([A-Z][A-Za-z\s]+)",
                r"([A-Z][A-Za-z\s]+) vs\.? ([A-Z][A-Za-z\s]+)"
            ],
            "ORGANIZATION": [
                r"([A-Z][A-Za-z\s]+) Pvt\. Ltd\.",
                r"([A-Z][A-Za-z\s]+) Limited",
                r"([A-Z][A-Za-z\s]+) LLP"
            ]
        }
        
        for entity_type, regex_patterns in patterns.items():
            for pattern in regex_patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    entities.append({
                        "text": match.group(0),
                        "label": entity_type,
                        "start": match.start(),
                        "end": match.end(),
                        "value": match.groups() if match.groups() else None
                    })
        
        return entities
    
    def _get_entity_description(self, label: str) -> str:
        """
        Get description for entity label
        
        Args:
            label (str): Entity label
            
        Returns:
            str: Description of the entity type
        """
        descriptions = {
            "PERSON": "Person's name",
            "ORG": "Organization or company",
            "GPE": "Geopolitical entity (country, city, state)",
            "MONEY": "Monetary values",
            "DATE": "Date or time",
            "LAW": "Legal act or law",
            "COURT": "Court name",
            "SECTION": "Legal section reference"
        }
        
        return descriptions.get(label, "Unknown entity type")
    
    def extract_clauses_and_relationships(self, text: str) -> Dict[str, Any]:
        """
        Extract clauses and their relationships
        
        Args:
            text (str): Text to analyze
            
        Returns:
            Dict[str, Any]: Clauses and relationships
        """
        clauses = []
        relationships = []
        
        # Extract clauses
        clause_patterns = [
            r'(\d+\.\s*[A-Z][^.]*?shall[^.]*\.)',
            r'(\d+\.\s*[A-Z][^.]*?agrees[^.]*\.)',
            r'(\d+\.\s*[A-Z][^.]*?warrants[^.]*\.)',
            r'(\d+\.\s*[A-Z][^.]*?represents[^.]*\.)'
        ]
        
        for pattern in clause_patterns:
            matches = re.finditer(pattern, text, re.MULTILINE)
            for match in matches:
                clause_text = match.group(1).strip()
                if len(clause_text) > 20:  # Filter out very short matches
                    clauses.append({
                        "text": clause_text,
                        "start": match.start(),
                        "end": match.end()
                    })
        
        # Extract relationships between clauses (simplified)
        for i in range(len(clauses) - 1):
            relationships.append({
                "from": i,
                "to": i + 1,
                "type": "sequential"
            })
        
        return {
            "clauses": clauses,
            "relationships": relationships
        }

# Global instance
entity_extractor = LegalEntityExtractor()