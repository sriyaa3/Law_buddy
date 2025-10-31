#!/usr/bin/env python3
"""
Test script for model router with smart routing
"""

from app.slm.model_router import model_router, ModelType

print("=" * 80)
print("TESTING MODEL ROUTER - SMART ROUTING")
print("=" * 80)

# Test cases
test_cases = [
    {
        "query": "a company has 1cr turnover. it has 20 employees with total salary expenditure of 20 lpa, resources are 50 lpa and rest is miscellaneous expenditure then what taxes do i have to pay? give me some legal advice too.",
        "expected_model": "LLM or CALC",
        "description": "Tax calculation query"
    },
    {
        "query": "What is MSME classification in India?",
        "expected_model": "SLM",
        "description": "Simple informational query"
    },
    {
        "query": "How to register for GST?",
        "expected_model": "SLM",
        "description": "MSME-specific simple query"
    },
    {
        "query": "Explain the complex legal framework for mergers and acquisitions in India with respect to competition law",
        "expected_model": "LLM",
        "description": "Complex reasoning query"
    },
    {
        "query": "Calculate income tax for turnover 5 crore and profit 50 lakhs",
        "expected_model": "LLM or CALC",
        "description": "Financial calculation"
    }
]

for i, test in enumerate(test_cases, 1):
    print(f"\n{'='*80}")
    print(f"TEST CASE {i}: {test['description']}")
    print(f"{'='*80}")
    print(f"Query: {test['query'][:100]}...")
    print(f"Expected Model: {test['expected_model']}")
    
    # Route the query
    model_type, reasoning = model_router.route_query(test['query'], "", "")
    
    print(f"\n✓ Routed to: {model_type.value.upper()}")
    print(f"✓ Reasoning: {reasoning}")
    
    # For calculation queries, test the calculation engine
    if model_type == ModelType.CALC or (model_type == ModelType.LLM and "calculation" in reasoning.lower()):
        print("\n[Testing Calculation Engine]")
        from app.slm.calculation_engine import calculation_engine
        financial_data = calculation_engine.extract_financial_data(test['query'])
        if financial_data:
            print(f"✓ Extracted financial data:")
            for key, value in financial_data.items():
                if isinstance(value, (int, float)):
                    print(f"  - {key}: ₹{value:,.2f}")

print("\n" + "=" * 80)
print("ROUTING TESTS COMPLETE")
print("=" * 80)
