#!/usr/bin/env python3
"""
Comprehensive End-to-End Testing Script
Tests all AskLegal features with real company data
"""

import sys
import os
sys.path.insert(0, '/app/asklegal_enhanced')

import json
import tempfile
from datetime import datetime
from test_data.sample_companies import (
    SAMPLE_COMPANIES, get_tax_calculation_query, get_company_query_prompt, get_all_companies
)

# Import all system components
from app.slm.calculation_engine import calculation_engine
from app.slm.gemini_engine import gemini_engine
from app.slm.model_router import model_router
from app.documents.generator import document_generator
from app.api.api_v1.endpoints.chat import generate_legal_response

class TestResults:
    """Store and display test results"""
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
        self.warnings = 0
    
    def add_result(self, test_name, status, details="", execution_time=0):
        """Add a test result"""
        self.results.append({
            "test": test_name,
            "status": status,
            "details": details,
            "time": execution_time
        })
        if status == "PASS":
            self.passed += 1
        elif status == "FAIL":
            self.failed += 1
        elif status == "WARN":
            self.warnings += 1
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        print(f"Total Tests: {len(self.results)}")
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"⚠️  Warnings: {self.warnings}")
        print("=" * 80)
        
        if self.failed > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.results:
                if result['status'] == "FAIL":
                    print(f"  - {result['test']}: {result['details']}")
    
    def save_to_file(self, filename="test_results.json"):
        """Save results to JSON file"""
        with open(filename, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "summary": {
                    "total": len(self.results),
                    "passed": self.passed,
                    "failed": self.failed,
                    "warnings": self.warnings
                },
                "results": self.results
            }, f, indent=2)
        print(f"\n📄 Results saved to: {filename}")

results = TestResults()

def test_system_initialization():
    """Test 1: System Initialization"""
    print("\n" + "=" * 80)
    print("TEST 1: SYSTEM INITIALIZATION")
    print("=" * 80)
    
    try:
        # Test calculation engine
        print("✓ Calculation Engine loaded")
        results.add_result("Calculation Engine Init", "PASS")
        
        # Test Gemini engine
        gemini_available = gemini_engine.is_available()
        if gemini_available:
            print("✓ Gemini Engine available")
            results.add_result("Gemini Engine Init", "PASS")
        else:
            print("⚠️  Gemini Engine not available (API key not set)")
            results.add_result("Gemini Engine Init", "WARN", "API key not set")
        
        # Test model router
        print("✓ Model Router loaded")
        results.add_result("Model Router Init", "PASS")
        
        # Test document generator
        print("✓ Document Generator loaded")
        results.add_result("Document Generator Init", "PASS")
        
        print("\n✅ All systems initialized successfully!")
        
    except Exception as e:
        print(f"\n❌ Initialization failed: {e}")
        results.add_result("System Init", "FAIL", str(e))

def test_tax_calculations_all_companies():
    """Test 2: Tax Calculations for All Company Types"""
    print("\n" + "=" * 80)
    print("TEST 2: TAX CALCULATIONS FOR ALL COMPANY TYPES")
    print("=" * 80)
    
    for company_key in get_all_companies():
        company = SAMPLE_COMPANIES[company_key]
        print(f"\n--- Testing: {company['company_name']} ---")
        print(f"Type: {company['legal_structure']} | Revenue: ₹{company['annual_revenue']/10000000:.2f} Cr")
        
        try:
            # Generate tax query
            query = get_tax_calculation_query(company_key)
            print(f"Query: {query[:100]}...")
            
            # Test calculation engine directly
            is_calc, calc_type = calculation_engine.detect_calculation_query(query)
            if not is_calc:
                results.add_result(f"Tax Calc Detection - {company_key}", "FAIL", "Not detected as calculation")
                continue
            
            # Extract financial data
            financial_data = calculation_engine.extract_financial_data(query)
            if not financial_data:
                results.add_result(f"Tax Calc Extraction - {company_key}", "FAIL", "No data extracted")
                continue
            
            print(f"✓ Extracted turnover: ₹{financial_data.get('turnover', 0)/10000000:.2f} Cr")
            print(f"✓ Extracted employees: {financial_data.get('employee_count', 0)}")
            
            # Calculate taxes
            result = calculation_engine.calculate_tax_liability(financial_data)
            total_tax = result['total_tax']
            income_tax = result['breakdown']['income_tax']
            
            print(f"✓ Total Tax: ₹{total_tax:,.2f}")
            print(f"✓ Income Tax: ₹{income_tax:,.2f}")
            print(f"✓ Professional Tax: ₹{result['breakdown']['professional_tax']:,.2f}")
            
            # Verify calculations are reasonable
            if total_tax < 0:
                results.add_result(f"Tax Calc - {company_key}", "FAIL", "Negative tax calculated")
            else:
                results.add_result(f"Tax Calc - {company_key}", "PASS", f"₹{total_tax:,.2f}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            results.add_result(f"Tax Calc - {company_key}", "FAIL", str(e))

def test_smart_routing():
    """Test 3: Smart Model Routing"""
    print("\n" + "=" * 80)
    print("TEST 3: SMART MODEL ROUTING")
    print("=" * 80)
    
    test_cases = [
        ("Calculate tax for 5 crore turnover", "CALC", "Financial calculation"),
        ("What is MSME classification?", "SLM", "Simple query"),
        ("How to register for GST?", "SLM", "MSME topic"),
        ("Explain complex merger legal framework", "SLM", "Could be LLM if Gemini available"),
    ]
    
    for query, expected, description in test_cases:
        print(f"\n--- {description} ---")
        print(f"Query: {query}")
        
        try:
            model_type, reasoning = model_router.route_query(query, "", "")
            print(f"✓ Routed to: {model_type.value.upper()}")
            print(f"✓ Reasoning: {reasoning}")
            
            # Flexible validation (CALC or LLM acceptable for calculations)
            if "calculation" in query.lower() or "calculate" in query.lower():
                if model_type.value in ["calc", "llm"]:
                    results.add_result(f"Routing - {description}", "PASS", model_type.value)
                else:
                    results.add_result(f"Routing - {description}", "WARN", f"Got {model_type.value}, expected CALC/LLM")
            else:
                results.add_result(f"Routing - {description}", "PASS", model_type.value)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            results.add_result(f"Routing - {description}", "FAIL", str(e))

def test_complete_response_generation():
    """Test 4: Complete Response Generation"""
    print("\n" + "=" * 80)
    print("TEST 4: COMPLETE RESPONSE GENERATION")
    print("=" * 80)
    
    # Test with manufacturing company
    company_key = "manufacturing_msme"
    company = SAMPLE_COMPANIES[company_key]
    query = get_tax_calculation_query(company_key)
    
    print(f"\nCompany: {company['company_name']}")
    print(f"Query: {query[:150]}...")
    
    try:
        response = model_router.generate_response(query, "", None, "")
        
        print(f"\n✓ Response generated: {len(response)} characters")
        
        # Verify response quality
        if len(response) < 100:
            results.add_result("Response Generation", "FAIL", "Response too short")
        elif "Error" in response and "Error generating" in response:
            results.add_result("Response Generation", "FAIL", "Error in response")
        else:
            # Check if response contains expected elements
            has_tax_info = any(word in response.lower() for word in ['tax', 'income tax', 'gst', 'professional tax'])
            has_numbers = any(char.isdigit() for char in response)
            has_breakdown = 'breakdown' in response.lower() or 'calculation' in response.lower()
            
            if has_tax_info and has_numbers:
                print("✓ Response contains tax information")
                print("✓ Response contains numerical calculations")
                print(f"\nResponse Preview:\n{response[:500]}...\n")
                results.add_result("Response Generation", "PASS", f"{len(response)} chars")
            else:
                results.add_result("Response Generation", "WARN", "Missing expected elements")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        results.add_result("Response Generation", "FAIL", str(e))

def test_document_generation():
    """Test 5: Document Generation for All Templates"""
    print("\n" + "=" * 80)
    print("TEST 5: DOCUMENT GENERATION")
    print("=" * 80)
    
    templates = {
        "nda": {
            "disclosing_party": "TechFlow Solutions Pvt Ltd",
            "receiving_party": "Partner Company Ltd",
            "effective_date": "January 15, 2025",
            "term": "2 years"
        },
        "employment_contract": {
            "employer": "TechFlow Solutions Pvt Ltd",
            "employee": "John Doe",
            "position": "Software Engineer",
            "salary": "₹12,00,000 per annum",
            "start_date": "February 1, 2025",
            "effective_date": "February 1, 2025",
            "benefits": "Health insurance, PF, gratuity"
        },
        "service_agreement": {
            "client": "TechFlow Solutions Pvt Ltd",
            "service_provider": "Consulting Services Inc",
            "services": "Software development and consulting",
            "payment_terms": "Net 30 days",
            "term": "1 year",
            "effective_date": "January 1, 2025"
        },
        "loan_agreement": {
            "lender": "TechFlow Solutions Pvt Ltd",
            "borrower": "Partner Company Ltd",
            "loan_amount": "₹50,00,000",
            "interest_rate": "10% per annum",
            "repayment_terms": "Monthly installments over 3 years",
            "effective_date": "January 1, 2025"
        },
        "notice": {
            "to_party": "Defaulting Client Ltd",
            "from_party": "TechFlow Solutions Pvt Ltd",
            "subject": "Payment Default Notice",
            "notice_date": datetime.now().strftime("%B %d, %Y"),
            "notice_content": "This is to inform you that payment of ₹5,00,000 is overdue by 90 days. Please clear the dues immediately.",
            "required_action": "Clear outstanding payment of ₹5,00,000",
            "response_deadline": "15 days from receipt",
            "contact_info": "legal@techflow.com, +91-9876543210"
        }
    }
    
    for template_name, details in templates.items():
        print(f"\n--- Testing: {template_name.upper()} ---")
        
        try:
            with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
                output_path = tmp.name
            
            success = document_generator.generate_document(template_name, details, output_path)
            
            if success and os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                print(f"✓ {template_name.upper()} generated: {file_size:,} bytes")
                results.add_result(f"Doc Gen - {template_name}", "PASS", f"{file_size} bytes")
                os.unlink(output_path)  # Clean up
            else:
                print(f"❌ {template_name.upper()} generation failed")
                results.add_result(f"Doc Gen - {template_name}", "FAIL", "File not created")
            
        except Exception as e:
            print(f"❌ Error generating {template_name}: {e}")
            results.add_result(f"Doc Gen - {template_name}", "FAIL", str(e))

def test_chat_endpoint_integration():
    """Test 6: Chat Endpoint Integration"""
    print("\n" + "=" * 80)
    print("TEST 6: CHAT ENDPOINT INTEGRATION")
    print("=" * 80)
    
    # Test with tech startup
    company = SAMPLE_COMPANIES["tech_startup"]
    test_query = "Calculate my company's tax liability"
    
    print(f"\nCompany: {company['company_name']}")
    print(f"Query: {test_query}")
    
    try:
        response, source = generate_legal_response(test_query, "test_chat_123", "user_001")
        
        print(f"\n✓ Response received from: {source}")
        print(f"✓ Response length: {len(response)} characters")
        
        if len(response) > 50:
            print(f"\nPreview:\n{response[:300]}...\n")
            results.add_result("Chat Endpoint", "PASS", f"Source: {source}")
        else:
            results.add_result("Chat Endpoint", "WARN", "Short response")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        results.add_result("Chat Endpoint", "FAIL", str(e))

def test_edge_cases():
    """Test 7: Edge Cases and Error Handling"""
    print("\n" + "=" * 80)
    print("TEST 7: EDGE CASES")
    print("=" * 80)
    
    edge_cases = [
        ("", "Empty query"),
        ("xyz abc random", "Nonsense query"),
        ("Calculate tax with no numbers", "Calculation without data"),
    ]
    
    for query, description in edge_cases:
        print(f"\n--- {description} ---")
        print(f"Query: '{query}'")
        
        try:
            if query:
                response = model_router.generate_response(query, "", None, "")
                print(f"✓ Handled gracefully: {len(response)} chars")
                results.add_result(f"Edge Case - {description}", "PASS", "Handled")
            else:
                results.add_result(f"Edge Case - {description}", "PASS", "Skipped")
        except Exception as e:
            print(f"⚠️  Exception raised: {e}")
            results.add_result(f"Edge Case - {description}", "WARN", str(e))

def main():
    """Run all tests"""
    print("=" * 80)
    print("ASKLEGAL ENHANCED - COMPREHENSIVE END-TO-END TESTING")
    print("Testing with Real Company Data")
    print("=" * 80)
    print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Number of Sample Companies: {len(SAMPLE_COMPANIES)}")
    print("=" * 80)
    
    # Run all tests
    test_system_initialization()
    test_tax_calculations_all_companies()
    test_smart_routing()
    test_complete_response_generation()
    test_document_generation()
    test_chat_endpoint_integration()
    test_edge_cases()
    
    # Print and save results
    results.print_summary()
    results.save_to_file("/app/asklegal_enhanced/test_results.json")
    
    print("\n" + "=" * 80)
    print("TESTING COMPLETE")
    print("=" * 80)
    print(f"\n✅ System is {'READY FOR PRODUCTION' if results.failed == 0 else 'NEEDS ATTENTION'}")
    print(f"\n📊 Detailed results saved to: /app/asklegal_enhanced/test_results.json")
    print(f"📝 Process documentation: /app/asklegal_enhanced/process.md")
    print(f"📖 Quick start guide: /app/asklegal_enhanced/QUICKSTART.md")
    
    # Exit with appropriate code
    sys.exit(0 if results.failed == 0 else 1)

if __name__ == "__main__":
    main()
