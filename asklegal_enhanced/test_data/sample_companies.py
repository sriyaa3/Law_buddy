"""
Sample Company Data for Testing AskLegal System
Contains realistic MSME company profiles
"""

SAMPLE_COMPANIES = {
    "tech_startup": {
        "company_name": "TechFlow Solutions Pvt Ltd",
        "industry": "Technology",
        "subcategory": "Software Development",
        "business_size": "Small",
        "location": "Bangalore, Karnataka",
        "employee_count": 25,
        "annual_revenue": 3.5 * 10000000,  # 3.5 Crore
        "legal_structure": "Private Limited",
        "incorporation_date": "2022-04-15",
        "registration_number": "U72900KA2022PTC156789",
        "gstin": "29AAACT1234F1Z5",
        "financial_data": {
            "turnover": 3.5 * 10000000,  # 3.5 Cr
            "salary_expense": 1.2 * 10000000,  # 1.2 Cr
            "resource_expense": 0.8 * 10000000,  # 0.8 Cr
            "misc_expense": 0.5 * 10000000,  # 0.5 Cr
            "profit_before_tax": 1.0 * 10000000  # 1 Cr
        },
        "test_queries": [
            "What are my tax obligations?",
            "Calculate tax liability for my company",
            "How to claim depreciation on software assets?",
            "What are the compliance requirements for a tech startup?",
            "Generate an NDA for our clients"
        ]
    },
    
    "manufacturing_msme": {
        "company_name": "Precision Engineering Works",
        "industry": "Manufacturing",
        "subcategory": "Automotive Parts",
        "business_size": "Medium",
        "location": "Pune, Maharashtra",
        "employee_count": 85,
        "annual_revenue": 25 * 10000000,  # 25 Crore
        "legal_structure": "Private Limited",
        "incorporation_date": "2018-08-10",
        "registration_number": "U29100MH2018PTC305123",
        "gstin": "27AABCP1234M1Z8",
        "financial_data": {
            "turnover": 25 * 10000000,  # 25 Cr
            "salary_expense": 4.5 * 10000000,  # 4.5 Cr
            "resource_expense": 12 * 10000000,  # 12 Cr (raw materials)
            "misc_expense": 3.5 * 10000000,  # 3.5 Cr (utilities, rent, etc.)
            "profit_before_tax": 5 * 10000000  # 5 Cr
        },
        "test_queries": [
            "Calculate complete tax liability with all expenses",
            "What are factory licensing requirements?",
            "How to manage GST for manufacturing business?",
            "Environmental clearance requirements for manufacturing",
            "Generate employment contract for factory worker"
        ]
    },
    
    "retail_business": {
        "company_name": "Green Mart Retail LLP",
        "industry": "Retail",
        "subcategory": "Organic Products",
        "business_size": "Small",
        "location": "Delhi",
        "employee_count": 15,
        "annual_revenue": 1.8 * 10000000,  # 1.8 Crore
        "legal_structure": "LLP",
        "incorporation_date": "2020-06-20",
        "registration_number": "AAR-5678",
        "gstin": "07AABFL1234Q1Z9",
        "financial_data": {
            "turnover": 1.8 * 10000000,  # 1.8 Cr
            "salary_expense": 0.4 * 10000000,  # 0.4 Cr
            "resource_expense": 0.9 * 10000000,  # 0.9 Cr (inventory)
            "misc_expense": 0.3 * 10000000,  # 0.3 Cr
            "profit_before_tax": 0.2 * 10000000  # 0.2 Cr
        },
        "test_queries": [
            "Calculate tax for retail business with 1.8 crore turnover",
            "Shop and establishment registration requirements",
            "Consumer protection compliance for retail",
            "How to get FSSAI license for food products?",
            "Generate service agreement with supplier"
        ]
    },
    
    "consulting_firm": {
        "company_name": "Business Consultants India",
        "industry": "Services",
        "subcategory": "Management Consulting",
        "business_size": "Small",
        "location": "Mumbai, Maharashtra",
        "employee_count": 12,
        "annual_revenue": 2.5 * 10000000,  # 2.5 Crore
        "legal_structure": "Partnership",
        "incorporation_date": "2019-03-15",
        "registration_number": None,  # Partnership doesn't require CIN
        "gstin": "27AABFB1234P1Z7",
        "financial_data": {
            "turnover": 2.5 * 10000000,  # 2.5 Cr
            "salary_expense": 0.8 * 10000000,  # 0.8 Cr
            "resource_expense": 0.2 * 10000000,  # 0.2 Cr (minimal)
            "misc_expense": 0.5 * 10000000,  # 0.5 Cr
            "profit_before_tax": 1.0 * 10000000  # 1 Cr
        },
        "test_queries": [
            "Tax calculation for partnership firm with 2.5 cr revenue",
            "Professional liability insurance requirements",
            "TDS implications for consultancy services",
            "How to draft client engagement agreement?",
            "Generate legal notice for payment default"
        ]
    },
    
    "micro_enterprise": {
        "company_name": "Home Baker's Paradise",
        "industry": "Food & Beverage",
        "subcategory": "Home-based Bakery",
        "business_size": "Micro",
        "location": "Jaipur, Rajasthan",
        "employee_count": 3,
        "annual_revenue": 0.4 * 10000000,  # 40 Lakhs
        "legal_structure": "Proprietorship",
        "incorporation_date": "2021-11-01",
        "registration_number": None,
        "gstin": None,  # Below 40 lakh threshold
        "financial_data": {
            "turnover": 0.4 * 10000000,  # 40 Lakhs
            "salary_expense": 0.06 * 10000000,  # 6 Lakhs
            "resource_expense": 0.20 * 10000000,  # 20 Lakhs
            "misc_expense": 0.08 * 10000000,  # 8 Lakhs
            "profit_before_tax": 0.06 * 10000000  # 6 Lakhs
        },
        "test_queries": [
            "Do I need GST registration with 40 lakh turnover?",
            "Income tax for proprietorship with 6 lakh profit",
            "FSSAI registration for home-based food business",
            "What is presumptive taxation under Section 44AD?",
            "Employee contract for part-time helper"
        ]
    }
}

def get_company_query_prompt(company_key: str, query: str) -> str:
    """
    Generate a complete query with company context
    
    Args:
        company_key: Key from SAMPLE_COMPANIES
        query: The query to ask
        
    Returns:
        Formatted query with context
    """
    company = SAMPLE_COMPANIES.get(company_key)
    if not company:
        return query
    
    context = f"""
Company: {company['company_name']}
Industry: {company['industry']}
Business Size: {company['business_size']}
Legal Structure: {company['legal_structure']}
Employees: {company['employee_count']}
Annual Revenue: ₹{company['annual_revenue']/10000000:.2f} Crore

Query: {query}
"""
    return context.strip()

def get_tax_calculation_query(company_key: str) -> str:
    """
    Generate a detailed tax calculation query for a company
    
    Args:
        company_key: Key from SAMPLE_COMPANIES
        
    Returns:
        Formatted tax calculation query
    """
    company = SAMPLE_COMPANIES.get(company_key)
    if not company or 'financial_data' not in company:
        return "Calculate my taxes"
    
    fd = company['financial_data']
    
    query = f"""
A {company['legal_structure']} company has:
- Turnover: ₹{fd['turnover']/10000000:.2f} crore
- {company['employee_count']} employees
- Salary expenditure: ₹{fd['salary_expense']/100000:.2f} lakhs
- Resource/material costs: ₹{fd['resource_expense']/100000:.2f} lakhs
- Miscellaneous expenses: ₹{fd['misc_expense']/100000:.2f} lakhs

Calculate the complete tax liability with:
1. Detailed breakdown of all taxes
2. Step-by-step methodology
3. Legal compliance requirements
4. Tax-saving opportunities
"""
    return query.strip()

def get_all_companies():
    """Get list of all company keys"""
    return list(SAMPLE_COMPANIES.keys())

def get_company_info(company_key: str):
    """Get full company information"""
    return SAMPLE_COMPANIES.get(company_key)
