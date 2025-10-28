import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from app.api.api_v1.endpoints.chat import generate_legal_response

def test_chat():
    print("Testing chat functionality...")
    
    # Test MSME query
    response, source = generate_legal_response("what is msme?", "test_chat")
    print(f"Query: what is msme?")
    print(f"Response: {response}")
    print(f"Source: {source}")
    print()
    
    # Test another query
    response, source = generate_legal_response("what are gst requirements for msme?", "test_chat")
    print(f"Query: what are gst requirements for msme?")
    print(f"Response: {response}")
    print(f"Source: {source}")
    print()
    
    print("Chat test completed!")

if __name__ == "__main__":
    test_chat()