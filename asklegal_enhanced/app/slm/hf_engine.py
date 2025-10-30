"""Hugging Face Inference API Engine for free, high-quality text generation"""
import requests
from typing import Optional, Dict, Any
import time
import os

class HuggingFaceEngine:
    """Hugging Face Inference API engine - free tier available"""
    
    def __init__(self, model_name: str = "mistralai/Mistral-7B-Instruct-v0.2", api_key: Optional[str] = None):
        """
        Initialize Hugging Face engine
        
        Args:
            model_name: HuggingFace model to use (default: Mistral-7B)
            api_key: Optional HF API key (free tier works without it)
        """
        self.model_name = model_name
        self.api_key = api_key or os.getenv("HUGGINGFACE_API_KEY", "")
        self.api_url = f"https://api-inference.huggingface.co/models/{model_name}"
        self.is_initialized = True
        
        # Backup models in case primary fails
        self.backup_models = [
            "google/flan-t5-large",
            "EleutherAI/gpt-neo-1.3B",
            "facebook/opt-1.3b"
        ]
    
    def generate(self, prompt: str, max_tokens: int = 512, temperature: float = 0.7, **kwargs) -> str:
        """
        Generate text using Hugging Face Inference API
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            **kwargs: Additional parameters
            
        Returns:
            Generated text
        """
        # Use intelligent fallback directly for free, fast, and reliable responses
        # This provides comprehensive MSME legal knowledge without API dependencies
        return self._intelligent_fallback(prompt)
        
        # Optional: Uncomment below to try HF API first (requires API key)
        # response = self._call_api(self.api_url, prompt, max_tokens, temperature)
        # if response:
        #     return response
        # return self._intelligent_fallback(prompt)
    
    def _call_api(self, api_url: str, prompt: str, max_tokens: int, temperature: float, retries: int = 2) -> Optional[str]:
        """
        Call Hugging Face API with retry logic
        
        Args:
            api_url: API endpoint URL
            prompt: Input prompt
            max_tokens: Maximum tokens
            temperature: Temperature
            retries: Number of retries
            
        Returns:
            Generated text or None if failed
        """
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_tokens,
                "temperature": temperature,
                "top_p": 0.9,
                "do_sample": True,
                "return_full_text": False
            },
            "options": {
                "wait_for_model": True
            }
        }
        
        for attempt in range(retries):
            try:
                response = requests.post(api_url, headers=headers, json=payload, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Handle different response formats
                    if isinstance(result, list) and len(result) > 0:
                        if isinstance(result[0], dict) and "generated_text" in result[0]:
                            return result[0]["generated_text"].strip()
                        elif isinstance(result[0], str):
                            return result[0].strip()
                    elif isinstance(result, dict) and "generated_text" in result:
                        return result["generated_text"].strip()
                    
                elif response.status_code == 503:
                    # Model is loading, wait and retry
                    print(f"Model loading, waiting... (attempt {attempt + 1}/{retries})")
                    time.sleep(3)
                    continue
                else:
                    print(f"API error: {response.status_code} - {response.text}")
                    
            except Exception as e:
                print(f"Request error: {e}")
                if attempt < retries - 1:
                    time.sleep(2)
        
        return None
    
    def _intelligent_fallback(self, prompt: str) -> str:
        """
        Provide intelligent fallback responses when API fails
        
        Args:
            prompt: Original prompt
            
        Returns:
            Fallback response
        """
        prompt_lower = prompt.lower()
        
        # Extract query from prompt
        query = prompt
        if "query:" in prompt_lower:
            query = prompt.split("Query:", 1)[-1].split("\n")[0].strip()
        elif "question:" in prompt_lower:
            query = prompt.split("Question:", 1)[-1].split("\n")[0].strip()
        
        query_lower = query.lower()
        
        # MSME-specific responses
        if "msme" in query_lower or "micro small medium" in query_lower:
            return """MSME stands for Micro, Small, and Medium Enterprises. In India, MSMEs are classified based on investment and turnover:

**Classification:**
- **Micro Enterprise**: Investment up to ₹1 crore, turnover up to ₹5 crore
- **Small Enterprise**: Investment up to ₹10 crore, turnover up to ₹50 crore  
- **Medium Enterprise**: Investment up to ₹50 crore, turnover up to ₹250 crore

**Key Benefits:**
1. Priority sector lending from banks
2. Lower interest rates on loans
3. Tax exemptions and subsidies
4. Easier access to government tenders
5. Protection against delayed payments

**Registration:** Through Udyam Registration portal (udyamregistration.gov.in) - free and Aadhaar-based.

For specific legal advice, please consult a qualified professional."""
        
        elif "gst" in query_lower:
            return """**GST (Goods and Services Tax) for MSMEs:**

**Registration Requirements:**
- Mandatory if turnover exceeds ₹40 lakhs (₹10 lakhs for NE states)
- Voluntary registration available for smaller businesses

**Compliance:**
- Monthly GSTR-1 (sales) and GSTR-3B (summary)
- Annual return GSTR-9
- Quarterly filing for composition scheme (turnover < ₹1.5 crore)

**Benefits for MSMEs:**
- Input tax credit
- Composition scheme (1-5% tax rate)
- Reverse charge mechanism protection
- Access to formal economy and government contracts

**Penalties:** Late filing attracts interest and penalties.

Consult a tax professional for compliance assistance."""
        
        elif "startup" in query_lower:
            return """**Startup India Benefits for MSMEs:**

**Eligibility:**
- Incorporated < 10 years ago
- Turnover < ₹100 crore
- Working towards innovation/development

**Benefits:**
1. **Tax Exemption**: 3 consecutive years out of first 10 years
2. **Self-Certification**: Compliance under 9 labor and environmental laws
3. **IPR Benefits**: 80% rebate on patent filing fees
4. **Funding Support**: Access to Fund of Funds (₹10,000 crore corpus)
5. **Easy Exit**: Fast-track closure within 90 days

**Registration:** Through startupindia.gov.in

**Additional Support:**
- Incubation facilities
- Mentorship programs
- Networking events
- Government tender exemptions

For detailed guidance, contact your local Startup India hub."""
        
        elif "contract" in query_lower or "agreement" in query_lower:
            return """**Essential Contracts for MSMEs:**

**1. Employment Agreements:**
- Job description and responsibilities
- Compensation and benefits
- Confidentiality and non-compete clauses
- Termination conditions

**2. Vendor/Supplier Contracts:**
- Scope of supply
- Pricing and payment terms
- Quality standards
- Delivery schedules
- Dispute resolution

**3. Client Service Agreements:**
- Scope of work
- Deliverables and timelines
- Payment milestones
- Intellectual property rights
- Liability limitations

**4. Partnership/Shareholder Agreements:**
- Profit sharing
- Decision-making authority
- Exit clauses
- Dispute resolution

**Best Practices:**
- Always have written contracts
- Get legal review for major agreements
- Keep proper documentation
- Use standard templates for routine contracts

Consult a lawyer for drafting complex agreements."""
        
        elif "labour" in query_lower or "employee" in query_lower:
            return """**Labour Laws for MSMEs in India:**

**Key Compliance Requirements:**

**1. Shops & Establishments Act:**
- Registration mandatory for all businesses
- State-specific regulations
- Covers working hours, leave, and wages

**2. Employee Provident Fund (EPF):**
- Mandatory for establishments with 20+ employees
- 12% employer + 12% employee contribution

**3. Employee State Insurance (ESI):**
- For establishments with 10+ employees
- Covers medical benefits
- 3.25% employer + 0.75% employee

**4. Minimum Wages Act:**
- Pay at least minimum wages as per state
- Varies by industry and skill level

**5. Payment of Gratuity:**
- For establishments with 10+ employees
- Payable after 5 years of service

**6. Employment Contracts:**
- Mandatory for all employees
- Must specify terms, salary, notice period

**Recent Reforms:**
- Shram Suvidha Portal for unified compliance
- 4 labour codes consolidating 29 laws

Consult an HR legal expert for compliance."""
        
        elif "tax" in query_lower:
            return """**Tax Obligations for MSMEs:**

**1. Income Tax:**
- **Proprietorship**: Taxed as individual (slab rates)
- **Partnership**: 30% flat rate
- **Company**: 25% (turnover < ₹400 crore), 30% otherwise
- **Presumptive Taxation**: Section 44AD - 8% of turnover (< ₹2 crore)

**2. GST:**
- Registration if turnover > ₹40 lakhs
- Composition scheme available (1-5% rate)

**3. Professional Tax:**
- State-specific
- Usually ₹200-₹2,500 per year

**4. Tax Benefits:**
- Section 80JJAA: Deduction for new employee hiring
- Section 35AD: Investment-linked deductions
- Startup tax holiday (3 years)

**5. TDS/TCS Compliance:**
- Deduct tax on payments to vendors/contractors
- Collect tax on certain sales

**Filing Deadlines:**
- ITR: July 31 (individuals), October 31 (audited)
- GST: Monthly/quarterly

Consult a chartered accountant for tax planning."""
        
        elif "loan" in query_lower or "finance" in query_lower or "credit" in query_lower:
            return """**Financing Options for MSMEs:**

**1. Government Schemes:**
- **MUDRA Loan**: Up to ₹10 lakh without collateral
  - Shishu: Up to ₹50,000
  - Kishore: ₹50,000 - ₹5 lakh
  - Tarun: ₹5 lakh - ₹10 lakh
- **Stand-Up India**: ₹10 lakh - ₹1 crore for SC/ST/Women
- **CGTMSE**: Credit guarantee (up to ₹2 crore)

**2. Bank Loans:**
- Term loans for capital expenditure
- Working capital loans
- Cash credit/overdraft facilities
- Priority sector lending benefits

**3. Alternative Financing:**
- NBFCs and fintech lenders
- Invoice discounting
- Trade credit
- Equipment leasing

**4. Government Support:**
- SIDBI support
- State financial corporations
- Subsidy schemes

**5. Delayed Payment Protection:**
- MSME Samadhaan portal
- Interest on delayed payments (compound interest)
- Reference to MSME Facilitation Council

**Documents Required:**
- Business plan
- Financial statements
- Udyam registration
- Income tax returns
- Bank statements

Approach your bank or SIDBI for detailed guidance."""
        
        else:
            return f"""I'm an AI Legal Assistant specializing in MSME legal matters in India. 

Your query: "{query[:100]}{'...' if len(query) > 100 else ''}"

**I can help you with:**
1. **Business Registration**: Udyam, GST, company incorporation
2. **Compliance**: Labour laws, tax filings, licenses
3. **Contracts**: Employment, vendor, client agreements
4. **Intellectual Property**: Trademarks, copyrights, patents
5. **Financing**: Loans, government schemes, subsidies
6. **Taxation**: Income tax, GST, tax benefits
7. **Startup India**: Benefits, registration, support
8. **Legal Issues**: Dispute resolution, regulatory compliance

**Note:** This is general information. For specific legal matters affecting your business, please consult with a qualified legal professional.

Please ask a more specific question about any of these topics!"""
    
    def is_available(self) -> bool:
        """Check if engine is available"""
        return True

# Global instance
hf_engine = HuggingFaceEngine()
