from typing import Optional, Dict, Any

class LocalInferenceEngine:
    """Simplified local inference engine - uses fallback responses"""
    
    def __init__(self, default_model: str = "fallback"):
        """
        Initialize the local inference engine
        
        Args:
            default_model (str): Default model to use for inference
        """
        self.default_model = default_model
        self.current_model = None
        self.engine = None
        self.is_initialized = True  # Always initialized with fallback
    
    def initialize(self, model_name: Optional[str] = None) -> bool:
        """
        Initialize the inference engine with a model
        
        Args:
            model_name (str, optional): Model to initialize with
            
        Returns:
            bool: True if initialization successful, False otherwise
        """
        # Simplified - always return True as we use fallback
        self.is_initialized = True
        return True
    
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
        # Return empty string to trigger fallback in model_router
        return ""
    
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