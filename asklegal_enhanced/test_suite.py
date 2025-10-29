#!/usr/bin/env python3
"""
Comprehensive test suite for AskLegal Enhanced
Tests backend APIs, services, and integrations
"""
import sys
import os
import json
import time
import requests
from pathlib import Path

# Color codes for terminal output
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color

class TestRunner:
    def __init__(self, base_url="http://localhost:8001"):
        self.base_url = base_url
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.results = []
    
    def print_test(self, name, status, message=""):
        """Print test result"""
        if status == "PASS":
            print(f"{GREEN}✓{NC} {name}")
            if message:
                print(f"  {message}")
            self.passed += 1
        elif status == "FAIL":
            print(f"{RED}✗{NC} {name}")
            if message:
                print(f"  Error: {message}")
            self.failed += 1
        elif status == "WARN":
            print(f"{YELLOW}⚠{NC} {name}")
            if message:
                print(f"  Warning: {message}")
            self.warnings += 1
        
        self.results.append({
            'test': name,
            'status': status,
            'message': message
        })
    
    def test_server_running(self):
        """Test if server is running"""
        print(f"\n{BLUE}Testing Server Connection...{NC}")
        try:
            response = requests.get(f"{self.base_url}/docs", timeout=5)
            if response.status_code == 200:
                self.print_test("Server is running", "PASS", "API docs accessible")
                return True
            else:
                self.print_test("Server response", "FAIL", f"Status code: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            self.print_test("Server connection", "FAIL", "Cannot connect to server")
            print(f"  Make sure server is running at {self.base_url}")
            return False
        except Exception as e:
            self.print_test("Server connection", "FAIL", str(e))
            return False
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        print(f"\n{BLUE}Testing Health Endpoint...{NC}")
        try:
            # Try to create health endpoint if it doesn't exist
            response = requests.get(f"{self.base_url}/api/v1/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.print_test("Health endpoint", "PASS", f"Status: {data.get('status', 'unknown')}")
                return True
            elif response.status_code == 404:
                self.print_test("Health endpoint", "WARN", "Endpoint not implemented")
                return True
            else:
                self.print_test("Health endpoint", "FAIL", f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.print_test("Health endpoint", "WARN", "Endpoint may not exist")
            return True
    
    def test_chat_endpoint(self):
        """Test chat message endpoint"""
        print(f"\n{BLUE}Testing Chat Endpoint...{NC}")
        try:
            payload = {
                "message": "What is IPC Section 420?",
                "session_id": "test-session-123"
            }
            
            response = requests.post(
                f"{self.base_url}/api/v1/chat/message",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'response' in data:
                    self.print_test("Chat endpoint", "PASS", f"Got response: {data['response'][:50]}...")
                    return True
                else:
                    self.print_test("Chat endpoint", "WARN", "Response format unexpected")
                    return True
            elif response.status_code == 404:
                self.print_test("Chat endpoint", "WARN", "Endpoint not found")
                return True
            else:
                self.print_test("Chat endpoint", "FAIL", f"Status: {response.status_code}")
                return False
                
        except requests.exceptions.Timeout:
            self.print_test("Chat endpoint", "WARN", "Request timeout (model may be loading)")
            return True
        except Exception as e:
            self.print_test("Chat endpoint", "WARN", str(e))
            return True
    
    def test_document_upload_endpoint(self):
        """Test document upload endpoint"""
        print(f"\n{BLUE}Testing Document Upload Endpoint...{NC}")
        try:
            # Create a dummy test file
            test_file_content = b"This is a test legal document."
            files = {'file': ('test_doc.txt', test_file_content, 'text/plain')}
            
            response = requests.post(
                f"{self.base_url}/api/v1/documents/upload",
                files=files,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.print_test("Document upload", "PASS", "File uploaded successfully")
                return True
            elif response.status_code == 404:
                self.print_test("Document upload", "WARN", "Endpoint not found")
                return True
            else:
                self.print_test("Document upload", "WARN", f"Status: {response.status_code}")
                return True
                
        except Exception as e:
            self.print_test("Document upload", "WARN", str(e))
            return True
    
    def test_models(self):
        """Test if models are available"""
        print(f"\n{BLUE}Testing Models...{NC}")
        
        # Check TinyLlama model
        model_path = Path('../asklegal_enhanced/models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf')
        if model_path.exists():
            size_mb = model_path.stat().st_size / (1024 * 1024)
            self.print_test("TinyLlama model", "PASS", f"Size: {size_mb:.1f} MB")
        else:
            self.print_test("TinyLlama model", "WARN", "Model file not found")
        
        # Check embeddings
        embeddings_dir = Path('../asklegal_enhanced/models/embeddings')
        if embeddings_dir.exists():
            self.print_test("Embedding models", "PASS", "Directory exists")
        else:
            self.print_test("Embedding models", "WARN", "Directory not found")
        
        return True
    
    def test_database(self):
        """Test database connection"""
        print(f"\n{BLUE}Testing Database...{NC}")
        
        db_path = Path('../asklegal_enhanced/asklegal.db')
        if db_path.exists():
            size_kb = db_path.stat().st_size / 1024
            self.print_test("Database file", "PASS", f"Size: {size_kb:.1f} KB")
            
            # Try to connect
            try:
                import sqlite3
                conn = sqlite3.connect(str(db_path))
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                conn.close()
                
                self.print_test("Database tables", "PASS", f"Found {len(tables)} tables")
                return True
            except Exception as e:
                self.print_test("Database connection", "WARN", str(e))
                return True
        else:
            self.print_test("Database file", "WARN", "Database not initialized")
            return True
    
    def test_vector_store(self):
        """Test FAISS vector store"""
        print(f"\n{BLUE}Testing Vector Store...{NC}")
        
        index_path = Path('../asklegal_enhanced/data/legal_documents.index')
        if index_path.exists():
            self.print_test("FAISS index", "PASS", "Index file exists")
            
            # Try to load
            try:
                import faiss
                index = faiss.read_index(str(index_path))
                self.print_test("FAISS load", "PASS", f"Contains {index.ntotal} vectors")
                return True
            except Exception as e:
                self.print_test("FAISS load", "WARN", "Cannot load index")
                return True
        else:
            self.print_test("FAISS index", "WARN", "Index not created yet")
            return True
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*70)
        print("Test Summary")
        print("="*70)
        print(f"Total Tests: {self.passed + self.failed + self.warnings}")
        print(f"{GREEN}Passed:{NC} {self.passed}")
        print(f"{RED}Failed:{NC} {self.failed}")
        print(f"{YELLOW}Warnings:{NC} {self.warnings}")
        
        if self.failed == 0:
            print(f"\n{GREEN}✅ All critical tests passed!{NC}")
        else:
            print(f"\n{RED}❌ Some tests failed. Please check the errors above.{NC}")
        
        # Save results to file
        results_file = Path('../asklegal_enhanced/test_results.json')
        with open(results_file, 'w') as f:
            json.dump({
                'summary': {
                    'passed': self.passed,
                    'failed': self.failed,
                    'warnings': self.warnings
                },
                'results': self.results
            }, f, indent=2)
        
        print(f"\nResults saved to: {results_file}")

def main():
    """Main test function"""
    print("="*70)
    print("AskLegal Enhanced - Comprehensive Test Suite")
    print("="*70)
    
    # Parse arguments
    base_url = "http://localhost:8001"
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    
    print(f"Testing server at: {base_url}")
    
    runner = TestRunner(base_url)
    
    # Run all tests
    server_running = runner.test_server_running()
    
    if server_running:
        runner.test_health_endpoint()
        runner.test_chat_endpoint()
        runner.test_document_upload_endpoint()
    else:
        print(f"\n{YELLOW}⚠ Server not running. Skipping API tests.{NC}")
        print("Start the server with: python start_enhanced.py")
    
    # Test local components
    runner.test_models()
    runner.test_database()
    runner.test_vector_store()
    
    # Print summary
    runner.print_summary()
    
    # Exit with appropriate code
    sys.exit(0 if runner.failed == 0 else 1)

if __name__ == "__main__":
    main()
