#!/usr/bin/env python3
"""
Simple test for chat functionality
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# Test the chat functionality
try:
    from app.api.api_v1.endpoints.chat import generate_legal_response
    print("Chat module loaded successfully")
    
    # Test a simple query
    response, source = generate_legal_response("what is msme?", "test_chat")
    print(f"Response: {response}")
    print(f"Source: {source}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()