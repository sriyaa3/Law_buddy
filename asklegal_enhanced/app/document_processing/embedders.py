from sentence_transformers import SentenceTransformer
from PIL import Image
import numpy as np
from typing import List, Union
import torch
from transformers import AutoTokenizer, AutoModel
import os

class InLegalBertEmbedder:
    """InLegalBERT embedder for legal documents"""
    
    def __init__(self, model_name: str = "law-ai/InLegalBERT"):
        """
        Initialize the InLegalBERT embedder
        
        Args:
            model_name (str): Name of the InLegalBERT model to use
        """
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        
        # Try to load the model
        try:
            print(f"Attempting to load InLegalBERT model: {model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModel.from_pretrained(model_name)
            self.model.eval()
            print(f"Successfully loaded InLegalBERT model: {model_name}")
        except Exception as e:
            print(f"Warning: Could not load InLegalBERT model {model_name}: {e}")
            print("Falling back to sentence-transformers/all-MiniLM-L6-v2")
            # Fallback to sentence transformer
            self.fallback_embedder = SentenceTransformer("all-MiniLM-L6-v2")
    
    def embed_text(self, text: str) -> np.ndarray:
        """
        Generate embedding for a text string using InLegalBERT
        
        Args:
            text (str): Input text
            
        Returns:
            np.ndarray: Text embedding vector
        """
        if self.model and self.tokenizer:
            try:
                # Tokenize input
                inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512, padding=True)
                
                # Get embeddings
                with torch.no_grad():
                    outputs = self.model(**inputs)
                    # Use CLS token embedding
                    embeddings = outputs.last_hidden_state[:, 0, :].numpy()
                
                return embeddings.flatten()
            except Exception as e:
                print(f"Error generating InLegalBERT embedding: {e}")
                # Fallback to sentence transformer
                return self.fallback_embedder.encode(text)
        else:
            # Use fallback embedder
            return self.fallback_embedder.encode(text)
    
    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for a list of text strings
        
        Args:
            texts (List[str]): List of input texts
            
        Returns:
            np.ndarray: Text embedding vectors
        """
        if self.model and self.tokenizer:
            try:
                embeddings = []
                for text in texts:
                    embedding = self.embed_text(text)
                    embeddings.append(embedding)
                return np.array(embeddings)
            except Exception as e:
                print(f"Error generating InLegalBERT embeddings: {e}")
                # Fallback to sentence transformer
                return self.fallback_embedder.encode(texts)
        else:
            # Use fallback embedder
            return self.fallback_embedder.encode(texts)

class TextEmbedder:
    """Text embedding service using InLegalBERT for legal documents"""
    
    def __init__(self, model_name: str = "law-ai/InLegalBERT"):
        """
        Initialize the text embedder
        
        Args:
            model_name (str): Name of the sentence transformer model to use
        """
        self.model_name = model_name
        # Initialize with fallback model to avoid loading issues
        try:
            self.inlegalbert = InLegalBertEmbedder(model_name)
        except Exception as e:
            print(f"Error initializing InLegalBERT, using fallback: {e}")
            self.inlegalbert = SentenceTransformer("all-MiniLM-L6-v2")
    
    def embed_text(self, text: str) -> np.ndarray:
        """
        Generate embedding for a text string
        
        Args:
            text (str): Input text
            
        Returns:
            np.ndarray: Text embedding vector
        """
        if isinstance(self.inlegalbert, InLegalBertEmbedder):
            return self.inlegalbert.embed_text(text)
        else:
            # Fallback embedder
            return self.inlegalbert.encode(text)
    
    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for a list of text strings
        
        Args:
            texts (List[str]): List of input texts
            
        Returns:
            np.ndarray: Text embedding vectors
        """
        if isinstance(self.inlegalbert, InLegalBertEmbedder):
            return self.inlegalbert.embed_texts(texts)
        else:
            # Fallback embedder
            return self.inlegalbert.encode(texts)

class ImageEmbedder:
    """Image embedding service (simplified implementation)"""
    
    def __init__(self):
        """Initialize the image embedder"""
        # For now, we'll use a simple approach that converts images to vectors
        # In a full implementation, we would use a proper image embedding model
        pass
    
    def embed_image(self, image_path: str) -> np.ndarray:
        """
        Generate embedding for an image (simplified)
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            np.ndarray: Image embedding vector (simplified)
        """
        # Load image
        image = Image.open(image_path)
        
        # Resize to a fixed size
        image = image.resize((224, 224))
        
        # Convert to numpy array and flatten
        image_array = np.array(image)
        if len(image_array.shape) == 3:
            # RGB image
            flattened = image_array.flatten()
        else:
            # Grayscale image, convert to 3 channels
            flattened = np.stack([image_array, image_array, image_array], axis=-1).flatten()
        
        # Normalize and reduce dimensionality
        normalized = flattened / 255.0
        # Simple averaging to reduce dimensions (this is a very simplified approach)
        reduced = np.mean(normalized.reshape(-1, 10), axis=1)
        
        return reduced

class MultimodalEmbedder:
    """Multimodal embedding service combining text and image embeddings"""
    
    def __init__(self):
        """Initialize the multimodal embedder"""
        self.text_embedder = TextEmbedder()
        self.image_embedder = ImageEmbedder()
    
    def embed_document_element(self, element: dict) -> np.ndarray:
        """
        Generate embedding for a document element
        
        Args:
            element (dict): Document element with 'text' and/or 'image' keys
            
        Returns:
            np.ndarray: Combined embedding vector
        """
        embeddings = []
        
        # Embed text if present
        if 'text' in element and element['text']:
            text_embedding = self.text_embedder.embed_text(element['text'])
            embeddings.append(text_embedding)
        
        # Embed image if present
        if 'image_path' in element and element['image_path']:
            image_embedding = self.image_embedder.embed_image(element['image_path'])
            # Normalize to match text embedding dimensions
            if len(image_embedding) < 384:  # Assuming text embedding dimension
                # Pad with zeros
                padded = np.pad(image_embedding, (0, 384 - len(image_embedding)))
                embeddings.append(padded)
            elif len(image_embedding) > 384:
                # Truncate
                truncated = image_embedding[:384]
                embeddings.append(truncated)
            else:
                embeddings.append(image_embedding)
        
        # Combine embeddings
        if len(embeddings) == 0:
            # Return zero vector if no content
            return np.zeros(384)
        elif len(embeddings) == 1:
            # Return single embedding
            return embeddings[0]
        else:
            # Average multiple embeddings
            return np.mean(embeddings, axis=0)
    
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