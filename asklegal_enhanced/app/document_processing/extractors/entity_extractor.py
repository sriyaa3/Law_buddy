from typing import List, Dict, Any
import re

class LegalEntityExtractor:
    """Simplified legal entity extractor using rule-based patterns"""
    
    def __init__(self):
        # No external dependencies needed
        print("Initialized simplified entity extractor (rule-based only)")
    
    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract legal entities from text using rule-based patterns
        
        Args:
            text (str): Text to analyze
            
        Returns:
            List[Dict[str, Any]]: Extracted entities
        """
        entities = []
        
        # Rule-based extraction for legal-specific entities
        legal_entities = self._extract_legal_entities(text)
        entities.extend(legal_entities)
        
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
        
        # Extract clauses with improved patterns that match our document structure
        clause_patterns = [
            r'(\d+\.\s*[A-Z][^.]*?shall[^.]*\.)',
            r'(\d+\.\s*[A-Z][^.]*?agrees[^.]*\.)',
            r'(\d+\.\s*[A-Z][^.]*?warrants[^.]*\.)',
            r'(\d+\.\s*[A-Z][^.]*?represents[^.]*\.)',
            r'(\d+\.\s*[A-Z][^.]*?payment[^.]*\.)',
            r'(\d+\.\s*[A-Z][^.]*?confidentiality[^.]*\.)',
            r'(\d+\.\s*[A-Z][^.]*?termination[^.]*\.)',
            r'(\d+\.\s*[A-Z][^.]*?dispute[^.]*\.)',
            r'(\d+\.\s*[A-Z][^.]*?intellectual property[^.]*\.)',
            r'(\d+\.\s*[A-Z][^.]*?services[^.]*\.)',
            r'(\d+\.\s*[A-Z][^.]*?term[^.]*\.)'
        ]
        
        # Also look for section headers
        section_patterns = [
            r'([A-Z][A-Za-z\s]+)\n\n',
            r'\n([A-Z][A-Za-z\s]+)\n'
        ]
        
        # Extract clause-like sentences
        for pattern in clause_patterns:
            matches = re.finditer(pattern, text, re.MULTILINE | re.IGNORECASE)
            for match in matches:
                clause_text = match.group(1).strip()
                if len(clause_text) > 20:  # Filter out very short matches
                    clauses.append({
                        "text": clause_text,
                        "start": match.start(),
                        "end": match.end()
                    })
        
        # Extract section headers as clauses
        for pattern in section_patterns:
            matches = re.finditer(pattern, text, re.MULTILINE)
            for match in matches:
                section_text = match.group(1).strip()
                if len(section_text) > 10 and len(section_text) < 50:  # Reasonable section header length
                    # Check if it's not already captured
                    already_captured = any(section_text.lower() in clause["text"].lower() for clause in clauses)
                    if not already_captured:
                        clauses.append({
                            "text": section_text,
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
        
        # Remove duplicates based on text content
        unique_clauses = []
        seen_texts = set()
        for clause in clauses:
            text_lower = clause["text"].lower()
            if text_lower not in seen_texts:
                unique_clauses.append(clause)
                seen_texts.add(text_lower)
        
        return {
            "clauses": unique_clauses,
            "relationships": relationships
        }

# Global instance
entity_extractor = LegalEntityExtractor()