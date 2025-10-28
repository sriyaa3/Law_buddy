#!/usr/bin/env python3
"""
Test script for SLM functionality
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from app.slm.engine import inference_engine

def test_slm():
    """Test SLM functionality"""
    print("Testing SLM functionality...")
    
    # Check if engine is initialized
    if not inference_engine.is_initialized:
        print("Engine not initialized. Trying to initialize...")
        if not inference_engine.initialize():
            print("Failed to initialize engine")
            return False
    
    # Test generation
    prompt = "What is MSME in India?"
    print(f"Testing with prompt: {prompt}")
    
    response = inference_engine.generate(prompt)
    print(f"Response: {response}")
    
    return True

if __name__ == "__main__":
    test_slm()