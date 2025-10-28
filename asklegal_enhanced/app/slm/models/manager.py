import os
import requests
from typing import Optional, Dict, Any
import hashlib

class ModelManager:
    """Model manager for downloading and managing SLMs"""
    
    def __init__(self, models_dir: str = "models"):
        """
        Initialize the model manager
        
        Args:
            models_dir (str): Directory to store models
        """
        self.models_dir = models_dir
        self.models_info = {
            "mistral-7b-instruct-v0.2.Q4_K_M": {
                "url": "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
                "size": "4.1GB",
                "sha256": "placeholder_sha256"
            },
            "phi-3-mini-4k-instruct-q4": {
                "url": "https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf",
                "size": "2.2GB",
                "sha256": "placeholder_sha256"
            },
            "tinyllama-1.1b-chat-v1.0.Q4_K_M": {
                "url": "https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
                "size": "0.7GB",
                "sha256": "placeholder_sha256"
            }
        }
        
        # Create models directory if it doesn't exist
        os.makedirs(self.models_dir, exist_ok=True)
    
    def list_available_models(self) -> Dict[str, Dict[str, Any]]:
        """
        List available models
        
        Returns:
            Dict[str, Dict[str, Any]]: Available models information
        """
        return self.models_info
    
    def is_model_downloaded(self, model_name: str) -> bool:
        """
        Check if a model is downloaded
        
        Args:
            model_name (str): Name of the model
            
        Returns:
            bool: True if model is downloaded, False otherwise
        """
        if model_name not in self.models_info:
            return False
        
        model_path = os.path.join(self.models_dir, f"{model_name}.gguf")
        return os.path.exists(model_path)
    
    def get_model_path(self, model_name: str) -> Optional[str]:
        """
        Get the path to a model file
        
        Args:
            model_name (str): Name of the model
            
        Returns:
            Optional[str]: Path to the model file, or None if not downloaded
        """
        if not self.is_model_downloaded(model_name):
            return None
        
        return os.path.join(self.models_dir, f"{model_name}.gguf")
    
    def download_model(self, model_name: str, force: bool = False) -> bool:
        """
        Download a model
        
        Args:
            model_name (str): Name of the model to download
            force (bool): Force download even if model exists
            
        Returns:
            bool: True if download successful, False otherwise
        """
        if model_name not in self.models_info:
            print(f"Model {model_name} not found in available models")
            return False
        
        if not force and self.is_model_downloaded(model_name):
            print(f"Model {model_name} already downloaded")
            return True
        
        model_info = self.models_info[model_name]
        url = model_info["url"]
        filename = f"{model_name}.gguf"
        filepath = os.path.join(self.models_dir, filename)
        
        print(f"Downloading {model_name} ({model_info['size']})...")
        print(f"URL: {url}")
        
        try:
            # Stream download to handle large files
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            # Get total file size
            total_size = int(response.headers.get('content-length', 0))
            
            with open(filepath, 'wb') as f:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        # Show progress
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(f"\rDownloaded: {downloaded}/{total_size} bytes ({percent:.1f}%)", end='')
            
            print(f"\nModel {model_name} downloaded successfully to {filepath}")
            return True
            
        except Exception as e:
            print(f"Error downloading model {model_name}: {e}")
            # Clean up partial download
            if os.path.exists(filepath):
                os.remove(filepath)
            return False
    
    def verify_model(self, model_name: str) -> bool:
        """
        Verify model integrity using SHA256 checksum
        
        Args:
            model_name (str): Name of the model to verify
            
        Returns:
            bool: True if model is valid, False otherwise
        """
        model_path = self.get_model_path(model_name)
        if not model_path:
            return False
        
        expected_sha256 = self.models_info[model_name].get("sha256")
        if not expected_sha256 or expected_sha256 == "placeholder_sha256":
            print(f"No SHA256 checksum available for {model_name}")
            return True  # Skip verification if no checksum
        
        print(f"Verifying {model_name}...")
        
        try:
            sha256_hash = hashlib.sha256()
            with open(model_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(chunk)
            
            actual_sha256 = sha256_hash.hexdigest()
            
            if actual_sha256.lower() == expected_sha256.lower():
                print(f"Model {model_name} verified successfully")
                return True
            else:
                print(f"Model {model_name} verification failed")
                print(f"Expected: {expected_sha256}")
                print(f"Actual: {actual_sha256}")
                return False
                
        except Exception as e:
            print(f"Error verifying model {model_name}: {e}")
            return False

# Global instance
model_manager = ModelManager()