"""
Gemini LLM Engine for complex calculations and reasoning
"""

import os
import google.generativeai as genai
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class GeminiEngine:
    """Gemini LLM engine for complex queries requiring calculations"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini engine
        
        Args:
            api_key: Google API key (reads from env if not provided)
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.model = None
        self.is_initialized = False
        
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                self.is_initialized = True
                logger.info("✓ Gemini engine initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini: {e}")
                self.is_initialized = False
        else:
            logger.warning("Google API key not found. Gemini engine unavailable.")
    
    def generate(self, prompt: str, max_tokens: int = 2048, temperature: float = 0.3, **kwargs) -> str:
        """
        Generate response using Gemini
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (lower = more focused)
            **kwargs: Additional parameters
            
        Returns:
            Generated text
        """
        if not self.is_initialized or not self.model:
            raise RuntimeError("Gemini engine not initialized. Please check API key.")
        
        try:
            generation_config = genai.types.GenerationConfig(
                max_output_tokens=max_tokens,
                temperature=temperature,
                top_p=0.9,
                top_k=40
            )
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            if response and response.text:
                return response.text
            else:
                return "Error: Empty response from Gemini"
                
        except Exception as e:
            logger.error(f"Gemini generation error: {e}")
            return f"Error generating response: {str(e)}"
    
    def generate_with_calculation_focus(self, query: str, financial_data: Dict[str, Any], context: str = "") -> str:
        """
        Generate response with focus on accurate calculations
        
        Args:
            query: User query
            financial_data: Extracted financial data
            context: Additional context
            
        Returns:
            Generated response with calculations
        """
        calculation_prompt = f"""You are an expert Indian Tax Consultant and Chartered Accountant specializing in MSME taxation.

User Query: {query}

Financial Data Extracted:
{self._format_financial_data(financial_data)}

Additional Context: {context}

Your task:
1. **Calculate exact tax amounts** with step-by-step methodology
2. Provide **detailed breakdown** of all applicable taxes
3. Include **specific tax rates** as per Indian tax laws (FY 2024-25)
4. Explain **calculation methodology** for each tax component
5. Provide **legal advice** on compliance requirements
6. Suggest **tax-saving opportunities**

Tax Components to Consider:
- **Income Tax** (Company/Partnership/Proprietorship rates)
- **GST** (if applicable to transactions)
- **Professional Tax** (state-specific)
- **TDS** on salaries and other payments
- **Other applicable taxes** based on business type

Format your response with:
✅ Clear section headings
✅ Exact numerical calculations
✅ Step-by-step methodology
✅ Legal compliance requirements
✅ Practical recommendations

**Important**: Provide EXACT numbers and calculations, not generic advice. Be precise and detailed.
"""
        
        return self.generate(calculation_prompt, max_tokens=2048, temperature=0.3)
    
    def _format_financial_data(self, data: Dict[str, Any]) -> str:
        """Format financial data for prompt"""
        if not data:
            return "No financial data extracted from query."
        
        formatted = []
        if 'turnover' in data:
            formatted.append(f"- Turnover/Revenue: ₹{data['turnover']:,.2f} ({data['turnover']/10000000:.2f} Crore)")
        if 'employee_count' in data:
            formatted.append(f"- Number of Employees: {data['employee_count']}")
        if 'salary_expense' in data:
            formatted.append(f"- Salary Expenditure: ₹{data['salary_expense']:,.2f} ({data['salary_expense']/100000:.2f} Lakhs)")
        if 'resource_expense' in data:
            formatted.append(f"- Resource/Material Costs: ₹{data['resource_expense']:,.2f} ({data['resource_expense']/100000:.2f} Lakhs)")
        if 'misc_expense' in data:
            formatted.append(f"- Miscellaneous Expenses: ₹{data['misc_expense']:,.2f}")
        
        return "\n".join(formatted) if formatted else "No specific financial data available."
    
    def is_available(self) -> bool:
        """Check if Gemini is available"""
        return self.is_initialized

# Global instance
gemini_engine = GeminiEngine()
