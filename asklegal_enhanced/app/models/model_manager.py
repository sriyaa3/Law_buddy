"""
Enhanced Model Manager for AI Law Buddy
Supports: Phi-3 (local), Mistral 7B (local), Gemini (fallback)
Privacy-aware routing with differential privacy
"""

import os
import logging
from typing import Optional, Dict, Any, Literal
from enum import Enum
import torch
from ctransformers import AutoModelForCausalLM
import google.generativeai as genai
from app.core.config_enhanced import settings

logger = logging.getLogger(__name__)

class ModelType(str, Enum):
    PHI3 = "phi3"
    MISTRAL = "mistral"
    GEMINI = "gemini"

class SensitivityLevel(str, Enum):
    HIGH = "high"        # Highly sensitive - use only local Phi-3
    MEDIUM = "medium"    # Moderately sensitive - use local Mistral
    LOW = "low"          # Non-sensitive - can use Gemini fallback

class PrivacyAwareModelManager:
    """
    Manages multiple LLMs with privacy-aware routing:
    - Phi-3: For sensitive queries (local only)
    - Mistral 7B: For complex reasoning (local only)
    - Gemini: Fallback for non-sensitive queries
    """
    
    def __init__(self):
        self.models: Dict[str, Any] = {}
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Initializing Model Manager on device: {self.device}")
        
        # Initialize models
        self._initialize_models()
        
    def _initialize_models(self):
        """Initialize all available models"""
        
        # Initialize Phi-3 (Local - for sensitive queries)
        try:
            if os.path.exists(settings.PHI3_MODEL_PATH):
                logger.info("Loading Phi-3 model (local)...")
                self.models[ModelType.PHI3] = AutoModelForCausalLM.from_pretrained(
                    settings.PHI3_MODEL_PATH,
                    model_type="llama",  # Phi-3 uses Llama architecture
                    gpu_layers=50 if self.device == "cuda" else 0,
                    context_length=4096,
                    max_new_tokens=512,
                    temperature=settings.TEMPERATURE,
                    top_p=settings.TOP_P,
                )
                logger.info("✓ Phi-3 model loaded successfully")
            else:
                logger.warning(f"Phi-3 model not found at {settings.PHI3_MODEL_PATH}")
        except Exception as e:
            logger.error(f"Failed to load Phi-3 model: {e}")
            
        # Initialize Mistral 7B (Local - for complex reasoning)
        try:
            if os.path.exists(settings.MISTRAL_MODEL_PATH):
                logger.info("Loading Mistral 7B model (local)...")
                self.models[ModelType.MISTRAL] = AutoModelForCausalLM.from_pretrained(
                    settings.MISTRAL_MODEL_PATH,
                    model_type="mistral",
                    gpu_layers=50 if self.device == "cuda" else 0,
                    context_length=8192,
                    max_new_tokens=1024,
                    temperature=settings.TEMPERATURE,
                    top_p=settings.TOP_P,
                )
                logger.info("✓ Mistral 7B model loaded successfully")
            else:
                logger.warning(f"Mistral model not found at {settings.MISTRAL_MODEL_PATH}")
        except Exception as e:
            logger.error(f"Failed to load Mistral model: {e}")
            
        # Initialize Gemini (Fallback)
        try:
            if settings.GOOGLE_API_KEY:
                genai.configure(api_key=settings.GOOGLE_API_KEY)
                self.models[ModelType.GEMINI] = genai.GenerativeModel('gemini-pro')
                logger.info("✓ Gemini model configured as fallback")
            else:
                logger.warning("Google API key not provided, Gemini fallback unavailable")
        except Exception as e:
            logger.error(f"Failed to configure Gemini: {e}")
    
    def classify_sensitivity(self, query: str) -> SensitivityLevel:
        """
        Classify query sensitivity level
        High sensitivity keywords indicate private/personal legal matters
        """
        query_lower = query.lower()
        
        # High sensitivity keywords
        high_sensitivity_keywords = [
            'personal', 'private', 'confidential', 'my case', 'my company',
            'salary', 'employee', 'termination', 'dispute', 'lawsuit',
            'divorce', 'property', 'inheritance', 'criminal', 'accused'
        ]
        
        # Check for high sensitivity
        if any(keyword in query_lower for keyword in high_sensitivity_keywords):
            return SensitivityLevel.HIGH
            
        # Medium sensitivity for complex legal queries
        if len(query.split()) > 20 or any(word in query_lower for word in ['compliance', 'regulation', 'license']):
            return SensitivityLevel.MEDIUM
            
        return SensitivityLevel.LOW
    
    def route_query(self, sensitivity: SensitivityLevel) -> ModelType:
        """
        Route query to appropriate model based on sensitivity
        Priority: Privacy > Performance
        """
        if sensitivity == SensitivityLevel.HIGH:
            # Use Phi-3 for sensitive queries
            if ModelType.PHI3 in self.models:
                return ModelType.PHI3
            elif ModelType.MISTRAL in self.models:
                return ModelType.MISTRAL
            else:
                logger.warning("No local model available for sensitive query")
                return ModelType.GEMINI
                
        elif sensitivity == SensitivityLevel.MEDIUM:
            # Use Mistral for complex reasoning
            if ModelType.MISTRAL in self.models:
                return ModelType.MISTRAL
            elif ModelType.PHI3 in self.models:
                return ModelType.PHI3
            else:
                return ModelType.GEMINI
                
        else:  # LOW sensitivity
            # Can use any model, prefer more capable ones
            if ModelType.MISTRAL in self.models:
                return ModelType.MISTRAL
            elif ModelType.GEMINI in self.models:
                return ModelType.GEMINI
            elif ModelType.PHI3 in self.models:
                return ModelType.PHI3
            else:
                raise RuntimeError("No models available")
    
    def generate(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        model_type: Optional[ModelType] = None,
        **kwargs
    ) -> str:
        """
        Generate response with privacy-aware model routing
        """
        # Classify sensitivity if model not explicitly specified
        if model_type is None:
            sensitivity = self.classify_sensitivity(prompt)
            model_type = self.route_query(sensitivity)
            logger.info(f"Query sensitivity: {sensitivity.value}, Routing to: {model_type.value}")
        
        # Get model
        model = self.models.get(model_type)
        if model is None:
            raise ValueError(f"Model {model_type} not available")
        
        # Set parameters
        max_tokens = max_tokens or settings.MAX_TOKENS
        temperature = temperature or settings.TEMPERATURE
        
        try:
            if model_type == ModelType.GEMINI:
                # Gemini API call
                response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=max_tokens,
                        temperature=temperature,
                    )
                )
                return response.text
            else:
                # Local model (Phi-3 or Mistral)
                response = model(
                    prompt,
                    max_new_tokens=max_tokens,
                    temperature=temperature,
                    **kwargs
                )
                return response
                
        except Exception as e:
            logger.error(f"Generation failed with {model_type}: {e}")
            # Fallback to next available model
            if model_type != ModelType.GEMINI and ModelType.GEMINI in self.models:
                logger.info("Falling back to Gemini")
                return self.generate(prompt, max_tokens, temperature, ModelType.GEMINI)
            raise
    
    def get_available_models(self) -> list[str]:
        """Return list of available models"""
        return list(self.models.keys())
    
    def is_model_available(self, model_type: ModelType) -> bool:
        """Check if specific model is available"""
        return model_type in self.models

# Global model manager instance
model_manager = None

def get_model_manager() -> PrivacyAwareModelManager:
    """Get or create model manager singleton"""
    global model_manager
    if model_manager is None:
        model_manager = PrivacyAwareModelManager()
    return model_manager
