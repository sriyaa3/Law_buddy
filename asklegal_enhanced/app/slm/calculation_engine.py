from typing import Dict, Any, Optional, Tuple
import re
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
    
    def _format_currency(self, amount: float) -> str:
        """
        Format currency in Indian format (Crores, Lakhs, Thousands)
        
        Args:
            amount (float): Amount to format
            
        Returns:
            str: Formatted currency string
        """
        if amount >= 10000000:  # Crores
            return f"₹{amount:,.2f} ({amount/10000000:.2f} Crore)"
        elif amount >= 100000:  # Lakhs
            return f"₹{amount:,.2f} ({amount/100000:.2f} Lakhs)"
        elif amount >= 1000:  # Thousands
            return f"₹{amount:,.2f} ({amount/1000:.2f} Thousand)"
        else:
            return f"₹{amount:,.2f}"
    
    def format_calculation_response(self, calculation_result: Dict[str, Any], query: str) -> str:
        """
        Format calculation result into human-readable response with proper line breaks
        
        Args:
            calculation_result (Dict[str, Any]): Calculation result
            query (str): Original query
            
        Returns:
            str: Formatted response
        """
        breakdown = calculation_result['breakdown']
        
        # Format the response with clean text formatting and proper line breaks
        response_lines = []
        
        # Header
        response_lines.append("TAX CALCULATION FOR YOUR MSME")
        response_lines.append("=" * 50)
        response_lines.append("")
        
        # Financial Summary
        response_lines.append("FINANCIAL SUMMARY:")
        response_lines.append("-" * 25)
        response_lines.append(f"Turnover: {self._format_currency(calculation_result['turnover'])}")
        response_lines.append("")
        
        # Expense Breakdown
        response_lines.append("EXPENSE BREAKDOWN:")
        response_lines.append("-" * 25)
        response_lines.append(f"1. Salary Expenditure: {self._format_currency(breakdown['salary_expense'])}")
        response_lines.append(f"2. Resource/Material Costs: {self._format_currency(breakdown['resource_expense'])}")
        response_lines.append(f"3. Miscellaneous Expenses: {self._format_currency(breakdown['misc_expense'])}")
        response_lines.append(f"4. Total Expenses: {self._format_currency(breakdown['total_expenses'])}")
        response_lines.append("")
        
        # Profit Calculation
        response_lines.append("PROFIT CALCULATION:")
        response_lines.append("-" * 25)
        response_lines.append(f"Profit Before Tax: {self._format_currency(breakdown['profit_before_tax'])}")
        response_lines.append("")
        
        # Tax Liability Breakdown
        response_lines.append("TAX LIABILITY BREAKDOWN:")
        response_lines.append("-" * 30)
        response_lines.append("")
        
        # Income Tax
        response_lines.append("1. Income Tax (Direct Tax on Profit)")
        response_lines.append(f"   • Tax Rate: {breakdown['income_tax_rate']*100:.0f}%")
        response_lines.append(f"   • Income Tax Payable: {self._format_currency(breakdown['income_tax'])}")
        response_lines.append(f"   • Calculation: {self._format_currency(breakdown['profit_before_tax'])} × {breakdown['income_tax_rate']*100:.0f}%")
        response_lines.append("")
        
        # Professional Tax
        response_lines.append("2. Professional Tax")
        response_lines.append(f"   • Per Employee: ₹{self.professional_tax:,}/year")
        response_lines.append(f"   • Total Professional Tax: {self._format_currency(breakdown['professional_tax'])}")
        response_lines.append("")
        
        # TDS on Salaries
        response_lines.append("3. TDS on Salaries (Deducted & Deposited)")
        response_lines.append(f"   • Rate: 10% (average)")
        response_lines.append(f"   • TDS Amount: {self._format_currency(breakdown['tds_on_salary'])}")
        response_lines.append(f"   • Note: This is deducted from employee salaries and deposited to government")
        response_lines.append("")
        
        # GST
        response_lines.append("4. GST (Goods & Services Tax)")
        response_lines.append(f"   • GST @ 18%: {self._format_currency(breakdown['gst_payable'])}")
        response_lines.append(f"   • Note: GST is typically passed on to customers and is NOT a direct cost to the company")
        response_lines.append("")
        
        # Total Direct Tax Liability
        response_lines.append("TOTAL DIRECT TAX LIABILITY:")
        response_lines.append("-" * 35)
        response_lines.append(f"{self._format_currency(calculation_result['total_tax'])}")
        response_lines.append("")
        response_lines.append("This includes:")
        response_lines.append(f"• Income Tax: {self._format_currency(breakdown['income_tax'])}")
        response_lines.append(f"• Professional Tax: {self._format_currency(breakdown['professional_tax'])}")
        response_lines.append("")
        
        # Net Profit After Tax
        response_lines.append("NET PROFIT AFTER TAX:")
        response_lines.append("-" * 27)
        response_lines.append(f"{self._format_currency(breakdown['profit_after_tax'])}")
        response_lines.append("")
        response_lines.append("=" * 50)
        response_lines.append("")
        
        # Legal Advice & Compliance
        response_lines.append("LEGAL ADVICE & COMPLIANCE:")
        response_lines.append("-" * 32)
        response_lines.append("")
        
        # Mandatory Compliances
        response_lines.append("Mandatory Compliances:")
        response_lines.append("1. Income Tax Return: File ITR-6 by October 31st")
        response_lines.append("2. GST Returns: Monthly GSTR-1 and GSTR-3B")
        response_lines.append("3. TDS Returns: Quarterly TDS returns (Form 24Q for salaries)")
        response_lines.append("4. Professional Tax: State-specific compliance")
        response_lines.append("5. Audit Requirement: Mandatory tax audit if turnover > ₹10 crore")
        response_lines.append("")
        
        # Tax-Saving Opportunities
        response_lines.append("Tax-Saving Opportunities:")
        response_lines.append("1. Section 80JJAA: Deduction for new employee hiring")
        response_lines.append("2. Section 35AD: Investment-linked deductions")
        response_lines.append("3. Depreciation: Claim depreciation on assets")
        response_lines.append("4. Business Expenses: Ensure all legitimate business expenses are accounted")
        response_lines.append("5. MAT Credit: Carry forward and utilize MAT credit if applicable")
        response_lines.append("")
        
        # Recommended Actions
        response_lines.append("Recommended Actions:")
        response_lines.append("1. Consult a Chartered Accountant for detailed tax planning")
        response_lines.append("2. Maintain proper books of accounts as per Companies Act")
        response_lines.append("3. Ensure timely TDS deduction and deposit")
        response_lines.append("4. Keep all supporting documents and invoices")
        response_lines.append("5. Consider tax-efficient salary structures for employees")
        response_lines.append("6. Explore government schemes for MSME tax benefits")
        response_lines.append("")
        
        # Important Notes
        response_lines.append("Important Notes:")
        response_lines.append("• This is a simplified calculation based on the information provided.")
        response_lines.append("• Actual tax liability may vary based on:")
        response_lines.append("  - Specific business type and industry")
        response_lines.append("  - Availability of deductions and exemptions")
        response_lines.append("  - State-specific taxes and regulations")
        response_lines.append("  - Advance tax payments already made")
        response_lines.append("  - Previous year losses that can be carried forward")
        response_lines.append("")
        response_lines.append("Professional Consultation Recommended:")
        response_lines.append("For accurate tax planning and compliance, please consult with a qualified")
        response_lines.append("Chartered Accountant who can review your complete financial statements.")
        response_lines.append("")
        response_lines.append("=" * 50)
        response_lines.append("")
        response_lines.append("Would you like me to provide more details on any specific aspect of taxation or compliance?")
        
        return "\n".join(response_lines)

# Global instance
calculation_engine = CalculationEngine()