"""
Test script to verify MSME-focused routing logic
"""

import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from app.msme.context.workflow import context_collector
from app.slm.model_router import model_router

def test_msme_routing():
    """Test MSME-focused routing logic"""
    
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
        "What government schemes are available for small manufacturing enterprises?",
        "Explain the complex legal precedents in international commercial litigation",  # Non-MSME query
        "Analyze the detailed implications of constitutional law on corporate governance"  # Complex non-MSME query
    ]
    
    print("\nTesting MSME-focused routing decisions:")
    print("=" * 60)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\nTest {i}: {query}")
        print("-" * 40)
        
        # Check routing decision
        model_type, reasoning = model_router.route_query(query, user_id=user_id)
        print(f"Routing Decision: {model_type.value}")
        print(f"Reasoning: {reasoning}")
        
        # Show MSME relevance score
        msme_relevance = model_router._calculate_msme_relevance(query, user_id)
        complexity_score = model_router._calculate_complexity(query, "")
        print(f"MSME Relevance Score: {msme_relevance:.2f}")
        print(f"Complexity Score: {complexity_score:.2f}")
    
    print("\n" + "=" * 60)
    print("MSME routing logic tests completed!")

if __name__ == "__main__":
    test_msme_routing()