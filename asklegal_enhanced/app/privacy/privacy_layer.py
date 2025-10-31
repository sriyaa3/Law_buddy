import re
from typing import Dict, Any, Tuple, Optional
from enum import Enum

class QuerySensitivity(Enum):
    """Query sensitivity levels"""
    PUBLIC = "public"
    SENSITIVE = "sensitive"
    HIGHLY_SENSITIVE = "highly_sensitive"

class PrivacyLayer:
    """Privacy layer for handling sensitive legal queries"""
    
    def __init__(self):
        # Define sensitive patterns
        self.sensitive_patterns = {
            "personal_identification": [
                r"\b(aadhar|aadhaar|pan|social security|ssn)\b",
                r"\b\d{12}\b",  # Aadhar-like numbers
                r"\b[A-Z]{5}\d{4}[A-Z]\b"  # PAN-like pattern
            ],
            "financial_information": [
                r"\b(account|bank|credit card|debit card)\b",
                r"\b\d{10,16}\b",  # Account/card numbers
                r"\b(ifsc|swift|bic)\b"
            ],
            "business_confidential": [
                r"\b(profit|loss|revenue|turnover|salary)\b",
                r"\b(confidential|proprietary|trade secret)\b"
            ]
        }
        
        # Define highly sensitive patterns
        self.highly_sensitive_patterns = {
            "legal_case_details": [
                r"\b(case no|court|judge|plaintiff|defendant)\b",
                r"\b(fir|complaint|petition)\b"
            ],
            "criminal_information": [
                r"\b(criminal|offense|crime|felony|misdemeanor)\b"
            ]
        }
        
        # Store the enum class reference
        self.QuerySensitivity = QuerySensitivity
    
    def classify_query_sensitivity(self, query: str) -> QuerySensitivity:
        """
        Classify query sensitivity level
        
        Args:
            query (str): User query
            
        Returns:
            QuerySensitivity: Sensitivity level
        """
        query_lower = query.lower()
        
        # Check for highly sensitive patterns
        for category, patterns in self.highly_sensitive_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    return QuerySensitivity.HIGHLY_SENSITIVE
        
        # Check for sensitive patterns
        for category, patterns in self.sensitive_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    return QuerySensitivity.SENSITIVE
        
        # Default to public
        return QuerySensitivity.PUBLIC
    
    def anonymize_text(self, text: str) -> str:
        """
        Anonymize sensitive information in text
        
        Args:
            text (str): Text to anonymize
            
        Returns:
            str: Anonymized text
        """
        # Replace Aadhar numbers (12 digits)
        text = re.sub(r"\b\d{12}\b", "[REDACTED_AADHAR]", text)
        
        # Replace PAN numbers (5 letters + 4 digits + 1 letter)
        text = re.sub(r"\b[A-Z]{5}\d{4}[A-Z]\b", "[REDACTED_PAN]", text)
        
        # Replace account numbers (10-16 digits)
        text = re.sub(r"\b\d{10,16}\b", "[REDACTED_ACCOUNT]", text)
        
        # Replace email addresses
        text = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[REDACTED_EMAIL]", text)
        
        # Replace phone numbers
        text = re.sub(r"\b\d{10}\b", "[REDACTED_PHONE]", text)
        text = re.sub(r"\b\d{3}-\d{3}-\d{4}\b", "[REDACTED_PHONE]", text)
        
        return text
    
    def route_query(self, query: str, user_context: Optional[Dict[str, Any]] = None) -> Tuple[str, str]:
        """
        Route query based on sensitivity and user context
        
        Args:
            query (str): User query
            user_context (Dict[str, Any], optional): User context information
            
        Returns:
            Tuple[str, str]: (response, processing_method)
        """
        sensitivity = self.classify_query_sensitivity(query)
        
        if sensitivity == QuerySensitivity.HIGHLY_SENSITIVE:
            return "This query contains highly sensitive information and requires special handling.", "highly_sensitive"
        elif sensitivity == QuerySensitivity.SENSITIVE:
            return "This query contains sensitive information.", "sensitive"
        else:
            return "This is a public query.", "public"
    
    def process_document(self, document_content: str, sensitivity_level: QuerySensitivity) -> str:
        """
        Process document based on sensitivity level
        
        Args:
            document_content (str): Document content
            sensitivity_level (QuerySensitivity): Sensitivity level
            
        Returns:
            str: Processed document content
        """
        if sensitivity_level == QuerySensitivity.HIGHLY_SENSITIVE:
            # Fully anonymize highly sensitive documents
            return self.anonymize_text(document_content)
        elif sensitivity_level == QuerySensitivity.SENSITIVE:
            # Partially anonymize sensitive documents
            return self.anonymize_text(document_content)
        else:
            # No anonymization for public documents
            return document_content

# Global instance
privacy_layer = PrivacyLayer()