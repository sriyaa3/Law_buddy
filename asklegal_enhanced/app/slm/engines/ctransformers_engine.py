from typing import Optional, Dict, Any
import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class HuggingFaceEngine:
    """SLM inference engine using Hugging Face transformers"""
    
    def __init__(self, model_name: Optional[str] = None):
        """
        Initialize the Hugging Face engine
        
        Args:
            model_name (str, optional): Name of the model to load
        """
        self.model_name = model_name or "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        self.model = None
        self.tokenizer = None
        
        # Default generation configuration
        self.config = {
            "max_new_tokens": 512,
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "repetition_penalty": 1.1
        }
        
        if model_name:
            self.load_model()
    
    def load_model(self):
        """Load the SLM model using Hugging Face transformers"""
        try:
            print(f"Loading model {self.model_name} with Hugging Face transformers...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            print(f"Model loaded successfully from {self.model_name}")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None
            self.tokenizer = None
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text using the SLM
        
        Args:
            prompt (str): Input prompt
            **kwargs: Additional generation parameters
            
        Returns:
            str: Generated text
        """
        if not self.model or not self.tokenizer:
            self.load_model()
            
        if not self.model:
            return "Error: Model not loaded"
        
        # Merge with default config
        generation_config = {**self.config, **kwargs}
        
        try:
            # Tokenize input
            inputs = self.tokenizer(prompt, return_tensors="pt")
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(**inputs, **generation_config)
            
            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Remove the prompt from the response (if present)
            if response.startswith(prompt):
                response = response[len(prompt):].strip()
            
            return response
        except Exception as e:
            print(f"Error generating response: {e}")
            return f"Error generating response: {e}"
    
    def is_loaded(self) -> bool:
        """Check if model is loaded"""
        return self.model is not None and self.tokenizer is not None

# Global instance (will be initialized when model is available)
slm_engine = HuggingFaceEngine()