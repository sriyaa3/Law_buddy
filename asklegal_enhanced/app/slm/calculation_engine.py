"""
Calculation Engine for Financial and Tax Queries
Handles MSME-specific tax calculations and financial computations
"""

import re
from typing import Dict, Any, Optional, Tuple
from enum import Enum

class CalculationType(str, Enum):
    """Types of calculations"""
    TAX = "tax"
    GST = "gst"
    SALARY = "salary"
    LOAN = "loan"
    PROFIT = "profit"
    GENERAL_FINANCIAL = "general_financial"

class CalculationEngine:
    """Engine for handling financial calculations for MSMEs"""
    
    def __init__(self):
        """Initialize calculation engine with tax rates and rules"""
        # Income Tax Rates for Companies (FY 2024-25)
        self.company_tax_rates = {
            "turnover_below_400cr": 0.25,  # 25%
            "turnover_above_400cr": 0.30   # 30%
        }
        
        # GST Rates
        self.gst_rates = {
            "standard": 0.18,
            "reduced": 0.12,
            "low": 0.05
        }
        
        # Professional Tax (varies by state, using average)
        self.professional_tax = 2500  # Annual per employee
        
        # TDS rates
        self.tds_rates = {
            "salary": 0.10,  # Average effective rate
            "contract": 0.02,
            "professional": 0.10
        }
        
    def detect_calculation_query(self, query: str) -> Tuple[bool, Optional[CalculationType]]:
        """
        Detect if query requires calculation
        
        Args:
            query (str): User query
            
        Returns:
            Tuple[bool, Optional[CalculationType]]: (is_calculation, calculation_type)
        """
        query_lower = query.lower()
        
        # Financial keywords
        calc_keywords = [
            "calculate", "computation", "how much", "what is the tax",
            "turnover", "revenue", "expenditure", "expenses", "profit",
            "salary", "cost", "amount", "pay", "tax liability",
            "net profit", "gross profit", "breakdown"
        ]
        
        # Check for calculation indicators
        has_calc_keyword = any(keyword in query_lower for keyword in calc_keywords)
        has_numbers = bool(re.search(r'\d+', query))
        
        if not (has_calc_keyword or has_numbers):
            return False, None
        
        # Detect calculation type
        if "tax" in query_lower or "income tax" in query_lower:
            return True, CalculationType.TAX
        elif "gst" in query_lower:
            return True, CalculationType.GST
        elif "salary" in query_lower or "employee" in query_lower:
            return True, CalculationType.SALARY
        elif "loan" in query_lower or "interest" in query_lower:
            return True, CalculationType.LOAN
        elif "profit" in query_lower:
            return True, CalculationType.PROFIT
        else:
            return True, CalculationType.GENERAL_FINANCIAL
    
    def extract_financial_data(self, query: str) -> Dict[str, Any]:
        """
        Extract financial data from query
        
        Args:
            query (str): User query
            
        Returns:
            Dict[str, Any]: Extracted financial data
        """
        data = {}
        
        # Extract turnover/revenue
        turnover_patterns = [
            r'(?:turnover|revenue)\s+(?:of|is)?\s*(?:rs\.?|₹)?\s*(\d+(?:\.\d+)?)\s*(cr|crore|lakh|lakhs?)',
            r'(\d+(?:\.\d+)?)\s*(cr|crore|lakh|lakhs?)\s+turnover',
            r'(\d+(?:\.\d+)?)\s*(cr|crore|lakh|lakhs?)\s+revenue'
        ]
        
        for pattern in turnover_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                amount = float(match.group(1))
                unit = match.group(2).lower()
                if 'cr' in unit:
                    data['turnover'] = amount * 10000000  # Convert to rupees
                elif 'lakh' in unit:
                    data['turnover'] = amount * 100000
                break
        
        # Extract employee count
        employee_patterns = [
            r'(\d+)\s+employees?',
            r'employees?:?\s*(\d+)',
            r'staff\s+of\s+(\d+)'
        ]
        
        for pattern in employee_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                data['employee_count'] = int(match.group(1))
                break
        
        # Extract salary expenditure
        salary_patterns = [
            r'salary\s+(?:expenditure|expense|cost)\s+(?:of|is)?\s*(?:rs\.?|₹)?\s*(\d+(?:\.\d+)?)\s*(cr|crore|lakh|lakhs?|lpa)',
            r'(\d+(?:\.\d+)?)\s*(lpa|lakh|lakhs?)\s+(?:salary|salaries)',
            r'total\s+salary\s+(?:of)?\s*(\d+(?:\.\d+)?)\s*(lpa|lakh)'
        ]
        
        for pattern in salary_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                amount = float(match.group(1))
                unit = match.group(2).lower()
                if 'cr' in unit:
                    data['salary_expense'] = amount * 10000000
                elif 'lpa' in unit or 'lakh' in unit:
                    data['salary_expense'] = amount * 100000
                break
        
        # Extract resource/material costs
        resource_patterns = [
            r'resources?\s+(?:are|is|cost)?\s*(?:rs\.?|₹)?\s*(\d+(?:\.\d+)?)\s*(cr|crore|lakh|lakhs?|lpa)',
            r'(\d+(?:\.\d+)?)\s*(lpa|lakh|lakhs?)\s+(?:resources?|materials?)'
        ]
        
        for pattern in resource_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                amount = float(match.group(1))
                unit = match.group(2).lower()
                if 'cr' in unit:
                    data['resource_expense'] = amount * 10000000
                elif 'lpa' in unit or 'lakh' in unit:
                    data['resource_expense'] = amount * 100000
                break
        
        # Extract miscellaneous expenses
        misc_patterns = [
            r'(?:miscellaneous|misc|other|rest)\s+(?:expenditure|expense|cost)?\s*(?:is)?\s*',
            r'rest\s+is\s+(?:miscellaneous|misc|other)\s+(?:expenditure|expense)'
        ]
        
        # If we have turnover and other expenses, calculate miscellaneous
        if 'turnover' in data:
            total_known_expenses = data.get('salary_expense', 0) + data.get('resource_expense', 0)
            # Assume remaining is miscellaneous (simplified)
            if total_known_expenses > 0:
                data['misc_expense'] = data['turnover'] - total_known_expenses
        
        return data
    
    def calculate_tax_liability(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate tax liability for MSME
        
        Args:
            financial_data (Dict[str, Any]): Financial data
            
        Returns:
            Dict[str, Any]: Tax calculation breakdown
        """
        result = {
            "turnover": financial_data.get('turnover', 0),
            "breakdown": {},
            "total_tax": 0,
            "detailed_explanation": []
        }
        
        # Calculate total expenses
        salary_expense = financial_data.get('salary_expense', 0)
        resource_expense = financial_data.get('resource_expense', 0)
        misc_expense = financial_data.get('misc_expense', 0)
        
        total_expenses = salary_expense + resource_expense + misc_expense
        
        # Calculate profit before tax
        profit_before_tax = result['turnover'] - total_expenses
        
        result['breakdown']['total_expenses'] = total_expenses
        result['breakdown']['salary_expense'] = salary_expense
        result['breakdown']['resource_expense'] = resource_expense
        result['breakdown']['misc_expense'] = misc_expense
        result['breakdown']['profit_before_tax'] = profit_before_tax
        
        # Calculate Income Tax
        turnover_in_cr = result['turnover'] / 10000000
        if turnover_in_cr < 400:
            income_tax_rate = self.company_tax_rates['turnover_below_400cr']
            result['detailed_explanation'].append(f"Company Income Tax Rate: 25% (turnover < ₹400 crore)")
        else:
            income_tax_rate = self.company_tax_rates['turnover_above_400cr']
            result['detailed_explanation'].append(f"Company Income Tax Rate: 30% (turnover ≥ ₹400 crore)")
        
        income_tax = profit_before_tax * income_tax_rate
        result['breakdown']['income_tax'] = income_tax
        result['breakdown']['income_tax_rate'] = income_tax_rate
        
        # Calculate GST (assuming standard rate on turnover)
        # Note: GST is typically passed on to customers, but included for reference
        gst_payable = result['turnover'] * self.gst_rates['standard']
        result['breakdown']['gst_payable'] = gst_payable
        result['detailed_explanation'].append(f"GST @ 18%: ₹{gst_payable:,.2f} (typically passed to customers)")
        
        # Calculate Professional Tax
        employee_count = financial_data.get('employee_count', 0)
        professional_tax = employee_count * self.professional_tax
        result['breakdown']['professional_tax'] = professional_tax
        result['detailed_explanation'].append(f"Professional Tax: {employee_count} employees × ₹{self.professional_tax:,} = ₹{professional_tax:,.2f}")
        
        # Calculate TDS on Salaries
        tds_on_salary = salary_expense * self.tds_rates['salary']
        result['breakdown']['tds_on_salary'] = tds_on_salary
        result['detailed_explanation'].append(f"TDS on Salaries @ 10%: ₹{tds_on_salary:,.2f} (deducted from employee salaries)")
        
        # Total Direct Tax Liability (Income Tax + Professional Tax)
        total_direct_tax = income_tax + professional_tax
        result['total_tax'] = total_direct_tax
        result['breakdown']['total_direct_tax'] = total_direct_tax
        
        # Calculate Profit After Tax
        profit_after_tax = profit_before_tax - income_tax
        result['breakdown']['profit_after_tax'] = profit_after_tax
        
        return result
    
    def format_calculation_response(self, calculation_result: Dict[str, Any], query: str) -> str:
        """
        Format calculation result into human-readable response
        
        Args:
            calculation_result (Dict[str, Any]): Calculation result
            query (str): Original query
            
        Returns:
            str: Formatted response
        """
        breakdown = calculation_result['breakdown']
        
        response = f"""# Tax Calculation for Your MSME

## Financial Summary:
**Turnover**: ₹{calculation_result['turnover']:,.2f} ({calculation_result['turnover']/10000000:.2f} Crore)

## Expense Breakdown:
1. **Salary Expenditure**: ₹{breakdown['salary_expense']:,.2f} ({breakdown['salary_expense']/100000:.2f} Lakhs)
2. **Resource/Material Costs**: ₹{breakdown['resource_expense']:,.2f} ({breakdown['resource_expense']/100000:.2f} Lakhs)
3. **Miscellaneous Expenses**: ₹{breakdown['misc_expense']:,.2f} ({breakdown['misc_expense']/100000:.2f} Lakhs)
4. **Total Expenses**: ₹{breakdown['total_expenses']:,.2f} ({breakdown['total_expenses']/10000000:.2f} Crore)

## Profit Calculation:
**Profit Before Tax**: ₹{breakdown['profit_before_tax']:,.2f} ({breakdown['profit_before_tax']/100000:.2f} Lakhs)

## Tax Liability Breakdown:

### 1. Income Tax (Direct Tax on Profit)
- **Tax Rate**: {breakdown['income_tax_rate']*100:.0f}%
- **Income Tax Payable**: ₹{breakdown['income_tax']:,.2f} ({breakdown['income_tax']/100000:.2f} Lakhs)
- **Calculation**: ₹{breakdown['profit_before_tax']:,.2f} × {breakdown['income_tax_rate']*100:.0f}%

### 2. Professional Tax
- **Per Employee**: ₹{self.professional_tax:,}/year
- **Total Professional Tax**: ₹{breakdown['professional_tax']:,.2f}

### 3. TDS on Salaries (Deducted & Deposited)
- **Rate**: 10% (average)
- **TDS Amount**: ₹{breakdown['tds_on_salary']:,.2f} ({breakdown['tds_on_salary']/100000:.2f} Lakhs)
- **Note**: This is deducted from employee salaries and deposited to government

### 4. GST (Goods & Services Tax)
- **GST @ 18%**: ₹{breakdown['gst_payable']:,.2f} ({breakdown['gst_payable']/10000000:.2f} Crore)
- **Note**: GST is typically passed on to customers and is NOT a direct cost to the company

## Total Direct Tax Liability:
**₹{calculation_result['total_tax']:,.2f} ({calculation_result['total_tax']/100000:.2f} Lakhs)**

This includes:
- Income Tax: ₹{breakdown['income_tax']:,.2f}
- Professional Tax: ₹{breakdown['professional_tax']:,.2f}

## Net Profit After Tax:
**₹{breakdown['profit_after_tax']:,.2f} ({breakdown['profit_after_tax']/100000:.2f} Lakhs)**

---

## Legal Advice & Compliance:

### Mandatory Compliances:
1. **Income Tax Return**: File ITR-6 by October 31st
2. **GST Returns**: Monthly GSTR-1 and GSTR-3B
3. **TDS Returns**: Quarterly TDS returns (Form 24Q for salaries)
4. **Professional Tax**: State-specific compliance
5. **Audit Requirement**: Mandatory tax audit if turnover > ₹10 crore

### Tax-Saving Opportunities:
1. **Section 80JJAA**: Deduction for new employee hiring
2. **Section 35AD**: Investment-linked deductions
3. **Depreciation**: Claim depreciation on assets
4. **Business Expenses**: Ensure all legitimate business expenses are accounted
5. **MAT Credit**: Carry forward and utilize MAT credit if applicable

### Recommended Actions:
1. ✅ Consult a Chartered Accountant for detailed tax planning
2. ✅ Maintain proper books of accounts as per Companies Act
3. ✅ Ensure timely TDS deduction and deposit
4. ✅ Keep all supporting documents and invoices
5. ✅ Consider tax-efficient salary structures for employees
6. ✅ Explore government schemes for MSME tax benefits

### Important Notes:
⚠️ **This is a simplified calculation** based on the information provided. Actual tax liability may vary based on:
- Specific business type and industry
- Availability of deductions and exemptions
- State-specific taxes and regulations
- Advance tax payments already made
- Previous year losses that can be carried forward

💼 **Professional Consultation Recommended**: For accurate tax planning and compliance, please consult with a qualified Chartered Accountant who can review your complete financial statements.

---

Would you like me to provide more details on any specific aspect of taxation or compliance?
"""
        
        return response

# Global instance
calculation_engine = CalculationEngine()
