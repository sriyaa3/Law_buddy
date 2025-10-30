from typing import Optional, Dict, Any
from app.slm.prompts.msme_legal_prompt import MSME_LEGAL_PROMPT_TEMPLATE, MSME_FALLBACK_PROMPT
import re

class LocalInferenceEngine:
    """Inference engine using Hugging Face API for high-quality responses"""
    
    def __init__(self, default_model: str = "huggingface"):
        """
        Initialize the inference engine
        
        Args:
            default_model (str): Default model to use for inference
        """
        self.default_model = default_model
        self.current_model = None
        self.engine = None
        self.is_initialized = False
        self._initialize_engine()
    
    def _initialize_engine(self):
        """Initialize Hugging Face engine"""
        try:
            from app.slm.hf_engine import hf_engine
            self.engine = hf_engine
            self.is_initialized = True
            print("✓ Hugging Face engine initialized successfully")
        except Exception as e:
            print(f"Warning: Could not initialize HF engine: {e}")
            self.is_initialized = False
    
    def initialize(self, model_name: Optional[str] = None) -> bool:
        """
        Initialize the inference engine with a model
        
        Args:
            model_name (str, optional): Model to initialize with
            
        Returns:
            bool: True if initialization successful, False otherwise
        """
        if not self.is_initialized:
            self._initialize_engine()
        return self.is_initialized
    
    def generate(self, prompt: str, model_name: Optional[str] = None, **kwargs) -> str:
        """
        Generate text using fallback responses (no model required)
        
        Args:
            prompt (str): Input prompt
            model_name (str, optional): Model to use for generation
            **kwargs: Additional generation parameters
            
        Returns:
            str: Generated text
        """
        # Check if this is an MSME legal prompt
        if "MSME" in prompt and ("legal matters" in prompt or "legal matters" in prompt.lower()):
            # Return a more detailed response for MSME queries
            return self._generate_msme_response(prompt)
        else:
            # Return a basic fallback response
            return "I'm an AI Legal Assistant specializing in MSME legal matters. I can help with business registration, compliance, contracts, intellectual property, employment law, and other legal issues specific to Micro, Small, and Medium Enterprises in India."
    
    def _generate_msme_response(self, prompt: str) -> str:
        """
        Generate a more detailed MSME-specific response
        
        Args:
            prompt (str): Input prompt
            
        Returns:
            str: Generated response
        """
        # Extract the query from the prompt using regex
        query = "General MSME legal query"
        
        # Try to extract query from different possible formats
        query_patterns = [
            r"User Query:\s*(.*?)\s*\n\n",
            r"Question:\s*(.*?)\s*\n\n",
            r"Query:\s*(.*?)\s*\n\n",
            r"User Query:\s*(.*?)$",
            r"Question:\s*(.*?)$",
            r"Query:\s*(.*?)$"
        ]
        
        # Clean the prompt to make extraction easier
        clean_prompt = prompt.replace('\r\n', '\n').replace('\r', '\n')
        
        for pattern in query_patterns:
            match = re.search(pattern, clean_prompt, re.DOTALL | re.IGNORECASE)
            if match:
                query = match.group(1).strip()
                # Remove any trailing instructions or formatting
                query = re.split(r'\n\s*\n', query)[0].strip()
                break
        
        # If we still have the default query, try to get the first meaningful line
        if query == "General MSME legal query":
            lines = clean_prompt.split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.startswith(('You are', 'Context:', 'Provide', 'Instructions:', 'Use the')):
                    # If this looks like a question, use it
                    if '?' in line or line.startswith(('What', 'How', 'Why', 'When', 'Where', 'Who', 'Can', 'Could', 'Should', 'Would', 'Is', 'Are', 'Do', 'Does')):
                        query = line
                        break
                    # Otherwise, if it's a reasonable length, use it
                    elif 10 <= len(line) <= 200:
                        query = line
                        break
        
        # Use the fallback prompt for a more structured response
        try:
            fallback_prompt = MSME_FALLBACK_PROMPT.format(query=query)
            response = fallback_prompt
        except Exception as e:
            # If formatting fails, return a direct response
            response = f"MSME stands for Micro, Small, and Medium Enterprises. In India, MSMEs are classified based on investment in plant and machinery/equipment and annual turnover. They play a crucial role in the Indian economy, contributing significantly to GDP, employment, and exports. Your specific query was about: {query}"
        
        return response
    
    def get_available_models(self) -> Dict[str, Dict[str, Any]]:
        """
        Get available models
        
        Returns:
            Dict[str, Dict[str, Any]]: Available models information
        """
        return {}
    
    def is_model_available(self, model_name: str) -> bool:
        """
        Check if a model is available (for compatibility)
        
        Args:
            model_name (str): Name of the model
            
        Returns:
            bool: True if model is available, False otherwise
        """
        return False

# Global instance
inference_engine = LocalInferenceEngine()