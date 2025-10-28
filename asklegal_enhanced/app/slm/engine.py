from typing import Optional, Dict, Any
from app.slm.models.manager import model_manager
from app.slm.engines.ctransformers_engine import HuggingFaceEngine

class LocalInferenceEngine:
    """Local inference engine that manages models and provides inference capabilities"""
    
    def __init__(self, default_model: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
        """
        Initialize the local inference engine
        
        Args:
            default_model (str): Default model to use for inference
        """
        self.default_model = default_model
        self.current_model = None
        self.engine = None
        self.is_initialized = False
    
    def initialize(self, model_name: Optional[str] = None) -> bool:
        """
        Initialize the inference engine with a model
        
        Args:
            model_name (str, optional): Model to initialize with
            
        Returns:
            bool: True if initialization successful, False otherwise
        """
        if not model_name:
            model_name = self.default_model
        
        print(f"Initializing inference engine with model: {model_name}")
        
        # For Hugging Face models, we don't need to check if they're downloaded
        # They will be downloaded automatically
        
        # Create and load engine
        try:
            self.engine = HuggingFaceEngine(model_name)
            if self.engine.is_loaded():
                self.current_model = model_name
                self.is_initialized = True
                print(f"Inference engine initialized with {model_name}")
                return True
            else:
                print(f"Failed to load model {model_name}")
                return False
        except Exception as e:
            print(f"Error initializing engine: {e}")
            return False
    
    def generate(self, prompt: str, model_name: Optional[str] = None, **kwargs) -> str:
        """
        Generate text using the SLM
        
        Args:
            prompt (str): Input prompt
            model_name (str, optional): Model to use for generation
            **kwargs: Additional generation parameters
            
        Returns:
            str: Generated text
        """
        # Initialize engine if not already done
        if not self.is_initialized:
            if not self.initialize(model_name):
                return "Error: Could not initialize inference engine."
        
        # Switch model if requested
        if model_name and model_name != self.current_model:
            if not self.initialize(model_name):
                return f"Error: Could not switch to model {model_name}"
        
        # Generate response
        if self.engine:
            return self.engine.generate(prompt, **kwargs)
        else:
            return "Error: Engine not initialized"
    
    def get_available_models(self) -> Dict[str, Dict[str, Any]]:
        """
        Get available models
        
        Returns:
            Dict[str, Dict[str, Any]]: Available models information
        """
        return model_manager.list_available_models()
    
    def is_model_available(self, model_name: str) -> bool:
        """
        Check if a model is available (for compatibility)
        
        Args:
            model_name (str): Name of the model
            
        Returns:
            bool: True if model is available, False otherwise
        """
        # For Hugging Face models, they're always available (will be downloaded)
        return True

# Global instance
inference_engine = LocalInferenceEngine()