#!/usr/bin/env python3
"""
Simple test for chat functionality
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

def test_simple_chat():
    print("Testing simple chat functionality...")
    
    try:
        # Test the SLM engine directly
        from app.slm.engine import inference_engine
        
        # Initialize the engine
        print("Initializing SLM engine...")
        result = inference_engine.initialize()
        print(f"Initialization result: {result}")
        print(f"Is initialized: {inference_engine.is_initialized}")
        
        if inference_engine.is_initialized:
            # Test generation
            print("Testing generation...")
            response = inference_engine.generate("What is MSME?", max_new_tokens=100)
            print(f"Response: {response}")
            return True
        else:
            print("Failed to initialize engine")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    test_simple_chat()