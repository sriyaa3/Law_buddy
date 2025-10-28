#!/usr/bin/env python3
"""
Script to download a lightweight SLM model for testing
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from app.slm.models.manager import model_manager

def download_test_model():
    """Download a lightweight model for testing"""
    print("Available models:")
    models = model_manager.list_available_models()
    for i, (name, info) in enumerate(models.items()):
        status = "✓ Downloaded" if model_manager.is_model_downloaded(name) else "○ Not downloaded"
        print(f"{i+1}. {name} ({info['size']}) - {status}")
    
    # Select the smallest model for testing
    test_model = "tinyllama-1.1b-chat-v1.0.Q4_K_M"
    
    if test_model in models:
        print(f"\nDownloading {test_model}...")
        success = model_manager.download_model(test_model)
        if success:
            print(f"✅ {test_model} downloaded successfully!")
            return True
        else:
            print(f"❌ Failed to download {test_model}")
            return False
    else:
        print(f"Model {test_model} not available in the model list")
        return False

def list_models():
    """List all available models and their status"""
    print("Available models:")
    models = model_manager.list_available_models()
    for i, (name, info) in enumerate(models.items()):
        status = "✓ Downloaded" if model_manager.is_model_downloaded(name) else "○ Not downloaded"
        print(f"{i+1}. {name} ({info['size']}) - {status}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        list_models()
    else:
        download_test_model()