"""
Simplified retriever for AskLegal Enhanced
Uses basic keyword matching without external dependencies
"""
import os
from pathlib import Path
from typing import List, Dict, Optional

class HybridRetriever:
    """Simplified retrieval system using keyword matching"""
    
    def __init__(self):
        self.index = None
        self.documents = []
        self.metadata = {}
        # No external dependencies required
        print("Initialized simplified retriever (no external dependencies)")
    
    def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Retrieve relevant documents for a query using simple keyword matching
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of relevant document chunks with scores
        """
        results = []
        
        # Simple keyword-based retrieval for MSME legal topics
        query_lower = query.lower()
        
        # Define some basic legal knowledge snippets for common MSME queries
        knowledge_base = {
            'gst': 'GST (Goods and Services Tax) is mandatory for businesses with turnover exceeding ₹40 lakhs (₹10 lakhs for northeastern states). MSMEs benefit from composition schemes and simplified returns.',
            'msme': 'MSMEs are classified based on investment and turnover: Micro (≤₹1cr investment, ≤₹5cr turnover), Small (≤₹10cr investment, ≤₹50cr turnover), Medium (≤₹50cr investment, ≤₹250cr turnover).',
            'registration': 'Udyam Registration is the primary registration for MSMEs in India. It provides benefits like lower interest rates, tax incentives, and easier access to government tenders.',
            'compliance': 'MSMEs must comply with various regulations including GST, income tax, labour laws, and industry-specific licenses. Simplified compliance through portals like Shram Suvidha.',
            'labour': 'Labour law compliance includes minimum wages, ESIC, PF, gratuity, and contracts. Businesses with 20+ employees need formal contracts and statutory registers.',
            'contract': 'Essential business contracts include employment agreements, vendor contracts, service agreements, and NDAs. Key clauses: scope, payment terms, liability, termination.',
            'trademark': 'Trademark registration protects brand names and logos. Online filing through IP India portal. MSMEs get subsidies on filing fees.',
            'loan': 'MSME financing options include MUDRA loans (up to ₹10L), CGTMSE (collateral-free loans), and SIDBI schemes. Priority sector lending benefits available.',
            'tax': 'MSMEs can opt for presumptive taxation (Section 44AD) if turnover <₹2cr. Regular taxation with business expense deductions for higher turnovers.'
        }
        
        # Match keywords from query
        for keyword, content in knowledge_base.items():
            if keyword in query_lower:
                results.append({
                    'content': content,
                    'score': 0.8,
                    'rank': len(results) + 1
                })
        
        # Fallback: return generic legal information
        if not results:
            results = [{
                'content': 'Indian MSME legal system covers various aspects including business registration, GST compliance, labour laws, contract management, and intellectual property protection. Please ask specific questions about these topics.',
                'score': 0.3,
                'rank': 1
            }]
        
        return results[:top_k]
    
    def get_context(self, query: str, max_length: int = 1000) -> str:
        """
        Get concatenated context for a query
        
        Args:
            query: Search query
            max_length: Maximum context length
            
        Returns:
            Concatenated context string
        """
        results = self.retrieve(query)
        
        context_parts = []
        current_length = 0
        
        for result in results:
            text = result['content']
            if current_length + len(text) <= max_length:
                context_parts.append(text)
                current_length += len(text)
            else:
                break
        
        return "\n\n".join(context_parts)

# Global instance
hybrid_retriever = HybridRetriever()