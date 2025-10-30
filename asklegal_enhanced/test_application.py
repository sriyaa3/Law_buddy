#!/usr/bin/env python3
"""
Test script to verify AskLegal Enhanced is working correctly
"""

import requests
import json
import sys
import time

BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api/v1"

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_success(text):
    print(f"✅ {text}")

def print_error(text):
    print(f"❌ {text}")

def test_health():
    """Test health endpoint"""
    print_header("Testing Health Endpoint")
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Health check passed: {data['status']}")
            print(f"   Version: {data['version']}")
            print(f"   Python: {data['python_version']}")
            print(f"   Components: {json.dumps(data['components'], indent=6)}")
            return True
        else:
            print_error(f"Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Health check failed: {e}")
        return False

def test_chat_api():
    """Test chat API"""
    print_header("Testing Chat API")
    
    test_questions = [
        "What is MSME?",
        "What are the GST requirements for small businesses?",
        "How do I register my business?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\nTest {i}: {question}")
        try:
            response = requests.post(
                f"{API_URL}/chat/message",
                json={"message": question, "chat_id": f"test_{i}"},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                print_success("Chat API responded")
                print(f"   Source: {data['source']}")
                print(f"   Response: {data['response'][:150]}...")
            else:
                print_error(f"Chat API failed with status {response.status_code}")
                return False
                
        except Exception as e:
            print_error(f"Chat API test failed: {e}")
            return False
    
    print_success("All chat tests passed!")
    return True

def test_frontend():
    """Test frontend is accessible"""
    print_header("Testing Frontend")
    try:
        response = requests.get(BASE_URL, timeout=5)
        if response.status_code == 200 and "AskLegal" in response.text:
            print_success("Frontend is accessible")
            return True
        else:
            print_error("Frontend check failed")
            return False
    except Exception as e:
        print_error(f"Frontend test failed: {e}")
        return False

def test_api_docs():
    """Test API documentation"""
    print_header("Testing API Documentation")
    try:
        response = requests.get(f"{API_URL}/docs", timeout=5)
        if response.status_code == 200:
            print_success("API documentation is accessible")
            return True
        else:
            print_error("API docs check failed")
            return False
    except Exception as e:
        print_error(f"API docs test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  AskLegal Enhanced - System Test")
    print("="*60)
    print(f"\nBase URL: {BASE_URL}")
    print(f"API URL: {API_URL}")
    
    # Wait a bit for server to be ready
    print("\nWaiting for server to be ready...")
    time.sleep(2)
    
    results = []
    
    # Run tests
    results.append(("Health Check", test_health()))
    results.append(("Frontend", test_frontend()))
    results.append(("API Documentation", test_api_docs()))
    results.append(("Chat API", test_chat_api()))
    
    # Summary
    print_header("Test Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Application is working correctly!")
        print("\n📍 Access the application at:")
        print(f"   Frontend: {BASE_URL}")
        print(f"   API Docs: {API_URL}/docs")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
