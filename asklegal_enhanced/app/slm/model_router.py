from typing import Dict, Any, Tuple, Optional
from app.slm.engine import inference_engine
from app.msme.context.workflow import context_collector
from app.msme.knowledge_base.industry_taxonomy import industry_taxonomy
from app.slm.prompts.msme_legal_prompt import MSME_LEGAL_PROMPT_TEMPLATE, MSME_FALLBACK_PROMPT
from app.slm.calculation_engine import calculation_engine, CalculationType
from app.slm.gemini_engine import gemini_engine
import os
import requests
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class ModelType(Enum):
    """Model types"""
    SLM = "slm"  # Small Language Model (local)
    LLM = "llm"  # Large Language Model (Gemini)
    CALC = "calc"  # Calculation engine

class ModelRouter:
    """Model router that selects appropriate model based on query complexity and MSME context"""
    
    def __init__(self):
        # Server LLM endpoint (would be configured in production)
        self.llm_endpoint = os.getenv("LLM_ENDPOINT", "http://localhost:8001/api/generate")
        self.llm_api_key = os.getenv("LLM_API_KEY", "")
        
        # Query complexity thresholds
        self.length_threshold = 100  # Characters
        self.complexity_keywords = [
            "analyze", "evaluate", "compare", "detailed", "comprehensive",
            "complex", "intricate", "nuanced", "interpret", "assess"
        ]
        self.legal_domain_keywords = [
            "contract", "litigation", "compliance", "regulation", "jurisdiction",
            "precedent", "statute", "tort", "liability", "damages"
        ]
        # MSME-specific keywords that should trigger SLM for domain expertise
        self.msme_keywords = [
            "msme", "udyam", "udyog aadhar", "micro enterprise", "small enterprise", 
            "medium enterprise", "gst", "mudra", "startup india", "sidbi",
            "labour law", "employee contract", "vendor agreement", "ip protection",
            "registration", "license", "tax", "loan", "credit", "insurance",
            "export", "import", "manufacturing", "retail", "services", "technology",
            "healthcare", "proprietary", "partnership", "llp", "private limited"
        ]
    
    def route_query(self, query: str, context: str = "", user_id: str = "") -> Tuple[ModelType, str]:
        """
        Route query to appropriate model based on complexity and MSME context
        Uses smart routing: Calculations -> Gemini, Simple queries -> SLM, Complex -> Gemini
        
        Args:
            query (str): User query
            context (str): Additional context
            user_id (str): User identifier for MSME context
            
        Returns:
            Tuple[ModelType, str]: (model_type, reasoning)
        """
        # First, check if this is a calculation query
        is_calculation, calc_type = calculation_engine.detect_calculation_query(query)
        
        if is_calculation:
            # Route calculation queries to Gemini for accurate responses
            if gemini_engine.is_available():
                return ModelType.LLM, f"Calculation query detected ({calc_type.value if calc_type else 'general'}), routing to Gemini for accuracy"
            else:
                # Fallback to calculation engine if Gemini unavailable
                return ModelType.CALC, f"Calculation query detected, using calculation engine (Gemini unavailable)"
        
        # For non-calculation queries, use existing logic with dynamic context
        complexity_score = self._calculate_complexity(query, context)
        msme_relevance = self._calculate_msme_relevance(query, user_id)
        
        # If query is highly relevant to MSME domain and simple, prefer SLM for domain expertise
        if msme_relevance > 0.7 and complexity_score < 0.5:
            return ModelType.SLM, f"High MSME relevance ({msme_relevance:.2f}), low complexity, routing to SLM for domain expertise"
        elif complexity_score > 0.7:
            # Complex queries go to Gemini if available
            if gemini_engine.is_available():
                return ModelType.LLM, f"High complexity score ({complexity_score:.2f}), routing to Gemini for better reasoning"
            else:
                return ModelType.SLM, f"High complexity but Gemini unavailable, using SLM"
        elif complexity_score > 0.4:
            # For medium complexity, consider MSME relevance
            if msme_relevance > 0.5:
                return ModelType.SLM, f"Medium complexity with MSME relevance, routing to SLM for domain expertise"
            else:
                if gemini_engine.is_available():
                    return ModelType.LLM, f"Medium complexity score ({complexity_score:.2f}), routing to Gemini for better reasoning"
                else:
                    return ModelType.SLM, f"Medium complexity but Gemini unavailable, using SLM"
        else:
            return ModelType.SLM, f"Low complexity score ({complexity_score:.2f}), routing to SLM for efficiency"
    
    def _calculate_complexity(self, query: str, context: str) -> float:
        """
        Calculate query complexity score (0.0 to 1.0)
        
        Args:
            query (str): User query
            context (str): Additional context
            
        Returns:
            float: Complexity score
        """
        score = 0.0
        query_lower = query.lower()
        
        # Length factor (0.3 weight)
        length_factor = min(len(query) / self.length_threshold, 1.0)
        score += length_factor * 0.3
        
        # Complexity keywords factor (0.3 weight)
        complexity_matches = sum(1 for keyword in self.complexity_keywords if keyword in query_lower)
        complexity_factor = min(complexity_matches / 3.0, 1.0)  # Max 3 keywords
        score += complexity_factor * 0.3
        
        # Legal domain factor (0.2 weight)
        legal_matches = sum(1 for keyword in self.legal_domain_keywords if keyword in query_lower)
        legal_factor = min(legal_matches / 3.0, 1.0)  # Max 3 keywords
        score += legal_factor * 0.2
        
        # Context factor (0.2 weight)
        if context:
            context_length_factor = min(len(context) / (self.length_threshold * 2), 1.0)
            score += context_length_factor * 0.2
        
        return min(score, 1.0)
    
    def _calculate_msme_relevance(self, query: str, user_id: str) -> float:
        """
        Calculate MSME relevance score (0.0 to 1.0)
        
        Args:
            query (str): User query
            user_id (str): User identifier
            
        Returns:
            float: MSME relevance score
        """
        score = 0.0
        query_lower = query.lower()
        
        # Check for MSME keywords (0.6 weight)
        msme_matches = sum(1 for keyword in self.msme_keywords if keyword in query_lower)
        msme_factor = min(msme_matches / 3.0, 1.0)  # Max 3 keywords
        score += msme_factor * 0.6
        
        # Check user's business context (0.4 weight)
        if user_id:
            business_context = context_collector.get_context_for_user(user_id)
            if business_context:
                # Industry-specific relevance
                industry = business_context.get("industry", "").lower()
                if industry and industry in query_lower:
                    score += 0.2
                
                # Business size relevance
                business_size = business_context.get("business_size", "").lower()
                if business_size and business_size in query_lower:
                    score += 0.1
                
                # Legal structure relevance
                legal_structure = business_context.get("legal_structure", "").lower()
                if legal_structure and legal_structure in query_lower:
                    score += 0.1
        
        return min(score, 1.0)
    
    def generate_response(self, query: str, context: str = "", model_preference: Optional[ModelType] = None, user_id: str = "") -> str:
        """
        Generate response using appropriate model with smart routing
        
        Args:
            query (str): User query
            context (str): Additional context
            model_preference (ModelType, optional): Preferred model type
            user_id (str): User identifier for MSME context
            
        Returns:
            str: Generated response
        """
        # Determine model to use
        if model_preference:
            model_type = model_preference
            reasoning = f"Using preferred model: {model_type.value}"
        else:
            model_type, reasoning = self.route_query(query, context, user_id)
        
        logger.info(f"Model routing: {reasoning}")
        print(f"Model routing: {reasoning}")
        
        # Route to appropriate engine
        if model_type == ModelType.CALC:
            return self._generate_with_calculation_engine(query, context)
        elif model_type == ModelType.LLM:
            return self._generate_with_gemini(query, context, user_id)
        else:
            return self._generate_with_slm(query, context, user_id)
    
    def _generate_with_calculation_engine(self, query: str, context: str) -> str:
        """
        Generate response using calculation engine for financial queries
        
        Args:
            query (str): User query
            context (str): Additional context
            
        Returns:
            str: Calculation response
        """
        try:
            # Extract financial data from query
            financial_data = calculation_engine.extract_financial_data(query)
            
            if not financial_data:
                return "I detected this as a financial calculation query, but couldn't extract specific numbers. Please provide:\n- Turnover/Revenue amount\n- Number of employees (if applicable)\n- Salary expenditure\n- Other expenses\n\nExample: 'A company has 1 crore turnover with 20 employees, salary expenditure of 20 lakhs, resources 50 lakhs'"
            
            # Calculate tax liability
            calculation_result = calculation_engine.calculate_tax_liability(financial_data)
            
            # Format response
            response = calculation_engine.format_calculation_response(calculation_result, query)
            
            return response
            
        except Exception as e:
            logger.error(f"Calculation engine error: {e}")
            return f"I encountered an error performing the calculation: {str(e)}\n\nPlease try rephrasing your query with clear financial figures."
    
    def _generate_with_gemini(self, query: str, context: str, user_id: str = "") -> str:
        """
        Generate response using Gemini LLM with dynamic context loading
        
        Args:
            query (str): User query
            context (str): Additional context
            user_id (str): User identifier for MSME context
            
        Returns:
            str: Generated response
        """
        try:
            # Check if this is a calculation query
            is_calculation, calc_type = calculation_engine.detect_calculation_query(query)
            
            if is_calculation:
                # For calculation queries, extract financial data
                financial_data = calculation_engine.extract_financial_data(query)
                
                # Get minimal MSME context for calculations
                minimal_context = self._get_minimal_context(user_id, "calculation")
                
                # Use Gemini with calculation-focused prompt
                response = gemini_engine.generate_with_calculation_focus(query, financial_data, minimal_context)
                return response
            else:
                # For complex reasoning queries, get relevant context
                relevant_context = self._get_dynamic_context(query, user_id, context)
                
                # Create comprehensive prompt
                prompt = f"""You are an expert AI Legal Assistant specializing in MSME legal matters in India.

{relevant_context}

Additional Context: {context}

User Query: {query}

Provide a detailed, accurate response based on Indian laws and MSME regulations. Include:
1. Relevant legal framework and regulations
2. Specific procedures and requirements
3. Compliance obligations
4. Practical recommendations
5. Government schemes and benefits (if applicable)

Keep your response focused, practical, and actionable for MSME owners.
"""
                
                response = gemini_engine.generate(prompt, max_tokens=2048, temperature=0.7)
                return response
                
        except Exception as e:
            logger.error(f"Gemini engine error: {e}, falling back to SLM")
            return self._generate_with_slm(query, context, user_id)
    
    def _get_minimal_context(self, user_id: str, query_type: str) -> str:
        """
        Get minimal context for specific query types (dynamic context loading)
        
        Args:
            user_id: User identifier
            query_type: Type of query (calculation, compliance, etc.)
            
        Returns:
            Minimal relevant context
        """
        if not user_id:
            return ""
        
        business_context = context_collector.get_context_for_user(user_id)
        if not business_context:
            return ""
        
        if query_type == "calculation":
            # For calculations, only include basic business info
            return f"""Business Context:
- Legal Structure: {business_context.get('legal_structure', 'N/A')}
- Business Size: {business_context.get('business_size', 'N/A')}
- Location: {business_context.get('location', 'N/A')}
"""
        else:
            return ""
    
    def _get_dynamic_context(self, query: str, user_id: str, existing_context: str) -> str:
        """
        Dynamically load only relevant context based on query type
        
        Args:
            query: User query
            user_id: User identifier
            existing_context: Existing context from retrieval
            
        Returns:
            Relevant context
        """
        query_lower = query.lower()
        context_parts = []
        
        # Determine what context is needed
        needs_business_context = any(word in query_lower for word in ['my', 'our', 'company', 'business'])
        needs_industry_context = any(word in query_lower for word in ['industry', 'sector', 'manufacturing', 'retail', 'services'])
        
        if user_id and needs_business_context:
            business_context = context_collector.get_context_for_user(user_id)
            if business_context:
                context_parts.append(f"""Business Context:
- Industry: {business_context.get('industry', 'N/A')}
- Business Size: {business_context.get('business_size', 'N/A')}
- Legal Structure: {business_context.get('legal_structure', 'N/A')}
- Location: {business_context.get('location', 'N/A')}
- Employee Count: {business_context.get('employee_count', 'N/A')}
""")
        
        if user_id and needs_industry_context:
            industry_insights = context_collector.get_industry_insights(user_id)
            if industry_insights:
                context_parts.append(f"""Industry Insights:
- Legal Requirements: {', '.join(industry_insights.get('legal_requirements', [])[:3])}
- Common Issues: {', '.join(industry_insights.get('common_issues', [])[:3])}
""")
        
        return "\n".join(context_parts) if context_parts else "No specific business context available."
    
    def _generate_with_slm(self, query: str, context: str, user_id: str = "") -> str:
        """
        Generate response using local SLM with dynamic MSME context
        
        Args:
            query (str): User query
            context (str): Additional context
            user_id (str): User identifier for MSME context
            
        Returns:
            str: Generated response
        """
        # Get minimal relevant context (dynamic loading)
        relevant_context = self._get_dynamic_context(query, user_id, context)
        
        # Use specialized MSME prompt template with only relevant context
        prompt = MSME_LEGAL_PROMPT_TEMPLATE.format(
            msme_context=relevant_context,
            context=context[:500] if context else "",  # Limit context size
            query=query
        )
        
        try:
            response = inference_engine.generate(prompt)
            # If we get an empty or error response, provide a more helpful fallback
            if not response or "Error:" in response or response.strip() == "":
                return self._get_contextual_fallback(query, context, relevant_context)
            return response
        except Exception as e:
            logger.error(f"Error with SLM: {e}")
            return self._get_contextual_fallback(query, context, relevant_context)
    
    def _get_contextual_fallback(self, query: str, context: str, msme_context: str = "") -> str:
        """
        Provide contextual fallback responses when SLM fails
        
        Args:
            query (str): User query
            context (str): Available context
            msme_context (str): MSME-specific context
            
        Returns:
            str: Contextual fallback response
        """
        # Try to extract relevant information from context
        if context and "Indian legal system" not in context:
            # If we have specific context, provide a response based on it
            return f"Based on the legal information available, here's what I can tell you about your query:\n\n{query}\n\nRelevant legal context:\n{context[:500]}...\n\nFor specific legal advice, please consult with a qualified legal professional."
        else:
            # Generic fallback with MSME focus using specialized prompt
            fallback_prompt = MSME_FALLBACK_PROMPT.format(query=query)
            try:
                response = inference_engine.generate(fallback_prompt)
                if response and not ("Error:" in response or response.strip() == ""):
                    return response
            except:
                pass
            # Final fallback
            return f"I specialize in helping MSMEs with legal matters in India. Your query: '{query}' relates to business law. I can assist with common MSME legal issues such as:\n- Business registration (Udyam, GST)\n- Compliance requirements\n- Employment and labor laws\n- Contract drafting\n- Intellectual property protection\n- Tax obligations\n- Access to finance\n- Export-import regulations\n\nPlease ask more specific questions about these topics, and I'll provide detailed guidance."

# Global instance
model_router = ModelRouter()