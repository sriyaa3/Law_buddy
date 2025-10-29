#!/usr/bin/env python3
"""
Test script for the AskLegal Enhanced chatbot
"""
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.api.api_v1.endpoints.chat import _get_fallback_response

def test_fallback_responses():
    """Test the fallback responses for various queries"""
    test_queries = [
        "What is article 17",
        "what is section 240?",
        "Startup India benefits",
        "Labour laws for small businesses"
    ]
    
    print("Testing fallback responses...")
    print("=" * 50)
    
    for query in test_queries:
        response = _get_fallback_response(query)
        print(f"Query: {query}")
        print(f"Response: {response[:100]}...")
        print("-" * 30)

if __name__ == "__main__":
    test_fallback_responses()