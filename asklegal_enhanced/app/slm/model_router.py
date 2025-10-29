from typing import Dict, Any, Tuple, Optional
from app.slm.engine import inference_engine
import os
import requests
from enum import Enum

class ModelType(Enum):
    """Model types"""
    SLM = "slm"  # Small Language Model (local)
    LLM = "llm"  # Large Language Model (server)

class ModelRouter:
    """Model router that selects appropriate model based on query complexity"""
    
    def __init__(self):
        # Server LLM endpoint (would be configured in production)
        self.llm_endpoint = os.getenv("LLM_ENDPOINT", "http://localhost:8001/api/generate")
        self.llm_api_key = os.getenv("LLM_API_KEY", "")
        
        # Query complexity thresholds
        self.length_threshold = 100  # Characters
        self.complexity_keywords = [
            "analyze", "evaluate", "compare", "detailed", "comprehensive",
            "complex", "intricate", "nuanced", "interpret", "assess"
        ]
        self.legal_domain_keywords = [
            "contract", "litigation", "compliance", "regulation", "jurisdiction",
            "precedent", "statute", "tort", "liability", "damages"
        ]
    
    def route_query(self, query: str, context: str = "") -> Tuple[ModelType, str]:
        """
        Route query to appropriate model based on complexity
        
        Args:
            query (str): User query
            context (str): Additional context
            
        Returns:
            Tuple[ModelType, str]: (model_type, reasoning)
        """
        complexity_score = self._calculate_complexity(query, context)
        
        if complexity_score > 0.7:
            return ModelType.LLM, f"High complexity score ({complexity_score:.2f}), routing to LLM"
        elif complexity_score > 0.4:
            return ModelType.LLM, f"Medium complexity score ({complexity_score:.2f}), routing to LLM for better reasoning"
        else:
            return ModelType.SLM, f"Low complexity score ({complexity_score:.2f}), routing to SLM for efficiency"
    
    def _calculate_complexity(self, query: str, context: str) -> float:
        """
        Calculate query complexity score (0.0 to 1.0)
        
        Args:
            query (str): User query
            context (str): Additional context
            
        Returns:
            float: Complexity score
        """
        score = 0.0
        query_lower = query.lower()
        
        # Length factor (0.3 weight)
        length_factor = min(len(query) / self.length_threshold, 1.0)
        score += length_factor * 0.3
        
        # Complexity keywords factor (0.3 weight)
        complexity_matches = sum(1 for keyword in self.complexity_keywords if keyword in query_lower)
        complexity_factor = min(complexity_matches / 3.0, 1.0)  # Max 3 keywords
        score += complexity_factor * 0.3
        
        # Legal domain factor (0.2 weight)
        legal_matches = sum(1 for keyword in self.legal_domain_keywords if keyword in query_lower)
        legal_factor = min(legal_matches / 3.0, 1.0)  # Max 3 keywords
        score += legal_factor * 0.2
        
        # Context factor (0.2 weight)
        if context:
            context_length_factor = min(len(context) / (self.length_threshold * 2), 1.0)
            score += context_length_factor * 0.2
        
        return min(score, 1.0)
    
    def generate_response(self, query: str, context: str = "", model_preference: Optional[ModelType] = None) -> str:
        """
        Generate response using appropriate model
        
        Args:
            query (str): User query
            context (str): Additional context
            model_preference (ModelType, optional): Preferred model type
            
        Returns:
            str: Generated response
        """
        # Determine model to use
        if model_preference:
            model_type = model_preference
            reasoning = f"Using preferred model: {model_type.value}"
        else:
            model_type, reasoning = self.route_query(query, context)
        
        print(f"Model routing: {reasoning}")
        
        if model_type == ModelType.LLM:
            return self._generate_with_llm(query, context)
        else:
            return self._generate_with_slm(query, context)
    
    def _generate_with_slm(self, query: str, context: str) -> str:
        """
        Generate response using local SLM
        
        Args:
            query (str): User query
            context (str): Additional context
            
        Returns:
            str: Generated response
        """
        prompt = f"""You are an AI Legal Assistant specializing in MSME legal matters in India.
        
Context: {context}

Query: {query}

Provide a detailed, accurate response based on the context and your knowledge of Indian MSME laws and regulations. If you don't have specific information, provide general guidance related to MSME legal matters.
"""
        
        try:
            response = inference_engine.generate(prompt)
            # If we get an empty or error response, provide a more helpful fallback
            if not response or "Error:" in response or response.strip() == "":
                return self._get_contextual_fallback(query, context)
            return response
        except Exception as e:
            print(f"Error with SLM: {e}")
            return self._get_contextual_fallback(query, context)
    
    def _get_contextual_fallback(self, query: str, context: str) -> str:
        """
        Provide contextual fallback responses when SLM fails
        
        Args:
            query (str): User query
            context (str): Available context
            
        Returns:
            str: Contextual fallback response
        """
        # Try to extract relevant information from context
        if context and "Indian legal system" not in context:
            # If we have specific context, provide a response based on it
            return f"Based on the legal information available, here's what I can tell you about your query:\n\n{query}\n\nRelevant legal context:\n{context[:500]}...\n\nFor specific legal advice, please consult with a qualified legal professional."
        else:
            # Generic fallback
            return f"I can help you with MSME legal matters in India. Your query: '{query}' relates to business law. While I don't have specific information on this topic right now, I can assist with common MSME legal issues such as business registration, compliance, taxation, labor laws, and intellectual property. Please ask more specific questions about these topics."
    
    def _generate_with_llm(self, query: str, context: str) -> str:
        """
        Generate response using server LLM
        
        Args:
            query (str): User query
            context (str): Additional context
            
        Returns:
            str: Generated response
        """
        try:
            # Prepare request payload
            payload = {
                "prompt": f"Context: {context}\n\nQuery: {query}\n\nProvide a detailed legal analysis:",
                "max_tokens": 1024,
                "temperature": 0.7
            }
            
            # Add API key if available
            headers = {}
            if self.llm_api_key:
                headers["Authorization"] = f"Bearer {self.llm_api_key}"
            
            # Make request to server LLM
            response = requests.post(self.llm_endpoint, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result.get("text", "No response text received")
            else:
                return f"Server LLM error: {response.status_code} - {response.text}"
                
        except Exception as e:
            # Fallback to SLM if server LLM fails
            print(f"Server LLM failed, falling back to SLM: {e}")
            return self._generate_with_slm(query, context)

# Global instance
model_router = ModelRouter()