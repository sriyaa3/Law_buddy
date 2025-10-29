import numpy as np
from typing import List, Union

class TextEmbedder:
    """Simplified text embedder without external model dependencies"""
    
    def __init__(self, model_name: str = "simplified"):
        """
        Initialize the text embedder
        
        Args:
            model_name (str): Model identifier (not used in simplified version)
        """
        self.model_name = model_name
        self.dimension = 384  # Standard embedding dimension
        print("Initialized simplified text embedder (no model required)")
    
    def embed_text(self, text: str) -> np.ndarray:
        """
        Generate simple hash-based embedding for a text string
        
        Args:
            text (str): Input text
            
        Returns:
            np.ndarray: Text embedding vector
        """
        # Simple hash-based embedding for demonstration
        # In production, you would use proper embeddings
        hash_value = hash(text)
        # Create a deterministic vector from the hash
        np.random.seed(abs(hash_value) % (2**32))
        embedding = np.random.rand(self.dimension).astype('float32')
        # Normalize
        embedding = embedding / np.linalg.norm(embedding)
        return embedding
    
    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for a list of text strings
        
        Args:
            texts (List[str]): List of input texts
            
        Returns:
            np.ndarray: Text embedding vectors
        """
        embeddings = []
        for text in texts:
            embeddings.append(self.embed_text(text))
        return np.array(embeddings)

class ImageEmbedder:
    """Simplified image embedder"""
    
    def __init__(self):
        """Initialize the image embedder"""
        self.dimension = 384
        print("Initialized simplified image embedder")
    
    def embed_image(self, image_path: str) -> np.ndarray:
        """
        Generate simple embedding for an image
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            np.ndarray: Image embedding vector
        """
        # Simple hash-based embedding
        hash_value = hash(image_path)
        np.random.seed(abs(hash_value) % (2**32))
        embedding = np.random.rand(self.dimension).astype('float32')
        embedding = embedding / np.linalg.norm(embedding)
        return embedding

class MultimodalEmbedder:
    """Simplified multimodal embedding service"""
    
    def __init__(self):
        """Initialize the multimodal embedder"""
        self.text_embedder = TextEmbedder()
        self.image_embedder = ImageEmbedder()
        self.dimension = 384
    
    def embed_document_element(self, element: dict) -> np.ndarray:
        """
        Generate embedding for a document element
        
        Args:
            element (dict): Document element with 'text' and/or 'image' keys
            
        Returns:
            np.ndarray: Combined embedding vector
        """
        # For simplicity, just use text embedding
        if 'text' in element and element['text']:
            return self.text_embedder.embed_text(element['text'])
        else:
            return np.zeros(self.dimension, dtype='float32')
    
    def embed_document_elements(self, elements: List[dict]) -> np.ndarray:
        """
        Generate embeddings for a list of document elements
        
        Args:
            elements (List[dict]): List of document elements
            
        Returns:
            np.ndarray: Embedding vectors for all elements
        """
        embeddings = []
        for element in elements:
            embedding = self.embed_document_element(element)
            embeddings.append(embedding)
        return np.array(embeddings)

# Global instances
text_embedder = TextEmbedder()
image_embedder = ImageEmbedder()
multimodal_embedder = MultimodalEmbedder()