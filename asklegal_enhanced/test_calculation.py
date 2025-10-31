#!/usr/bin/env python3
"""
Test script for calculation engine
"""

from app.slm.calculation_engine import calculation_engine

# Test query from user
test_query = "a company has 1cr turnover. it has 20 employees with total salary expenditure of 20 lpa, resources are 50 lpa and rest is miscellaneous expenditure then what taxes do i have to pay?"

print("=" * 80)
print("TESTING CALCULATION ENGINE")
print("=" * 80)
print(f"\nQuery: {test_query}\n")

# Test 1: Detect calculation query
is_calc, calc_type = calculation_engine.detect_calculation_query(test_query)
print(f"✓ Is Calculation Query: {is_calc}")
print(f"✓ Calculation Type: {calc_type}\n")

# Test 2: Extract financial data
financial_data = calculation_engine.extract_financial_data(test_query)
print("✓ Extracted Financial Data:")
for key, value in financial_data.items():
    if isinstance(value, (int, float)):
        print(f"  - {key}: ₹{value:,.2f}")
    else:
        print(f"  - {key}: {value}")

# Test 3: Calculate tax liability
calculation_result = calculation_engine.calculate_tax_liability(financial_data)
print(f"\n✓ Total Tax Liability: ₹{calculation_result['total_tax']:,.2f}")
print(f"✓ Profit After Tax: ₹{calculation_result['breakdown']['profit_after_tax']:,.2f}")

# Test 4: Format response
response = calculation_engine.format_calculation_response(calculation_result, test_query)
print("\n" + "=" * 80)
print("FORMATTED RESPONSE")
print("=" * 80)
print(response)
