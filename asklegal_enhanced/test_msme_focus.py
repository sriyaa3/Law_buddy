"""
Test script to verify MSME-focused SLM enhancements
"""

import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from app.msme.context.workflow import context_collector
from app.slm.model_router import model_router

def test_msme_enhancements():
    """Test MSME-focused enhancements"""
    
    # Create a test business profile
    test_profile = {
        "business_name": "Test Manufacturing Company",
        "industry": "manufacturing",
        "business_size": "small",
        "location": "Mumbai, Maharashtra",
        "legal_structure": "private_limited",
        "employee_count": 25,
        "contact_person": "John Doe",
        "contact_email": "john@testcompany.com",
        "contact_phone": "9876543210"
    }
    
    # Collect business profile
    user_id = "test_user_001"
    profile = context_collector.collect_business_profile(user_id, test_profile)
    print(f"Created business profile for: {profile.business_name}")
    
    # Test MSME-focused queries
    test_queries = [
        "What are the GST registration requirements for a small manufacturing company?",
        "Do I need a factory license for my manufacturing business with 25 employees?",
        "What are the labor law compliance requirements for a private limited company?",
        "How can I protect my product design as intellectual property?",
        "What government schemes are available for small manufacturing enterprises?"
    ]
    
    print("\nTesting MSME-focused queries:")
    print("=" * 50)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\nTest {i}: {query}")
        print("-" * 30)
        
        # Test with user context
        response = model_router.generate_response(query, user_id=user_id)
        print(f"Response: {response[:200]}...")  # Show first 200 characters
        
        # Check routing decision
        model_type, reasoning = model_router.route_query(query, user_id=user_id)
        print(f"Routing: {reasoning}")
    
    print("\n" + "=" * 50)
    print("MSME enhancement tests completed!")

if __name__ == "__main__":
    test_msme_enhancements()