#!/usr/bin/env python3
"""
Test script for chat functionality
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

def test_chat_functionality():
    print("Testing chat functionality...")
    
    try:
        from app.api.api_v1.endpoints.chat import generate_legal_response
        
        # Test with a simple MSME query
        response, source = generate_legal_response("What is MSME?", "test_chat_id")
        print(f"Response: {response}")
        print(f"Source: {source}")
        
        if response and not response.startswith("Error:"):
            print("✅ Chat functionality is working!")
            return True
        else:
            print("❌ Chat functionality is not working properly")
            return False
            
    except Exception as e:
        print(f"❌ Error in chat functionality: {e}")
        return False

if __name__ == "__main__":
    test_chat_functionality()