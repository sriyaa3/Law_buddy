from typing import Dict, List, Any, Optional
from app.msme.context.workflow import context_collector
from app.msme.knowledge_base.industry_taxonomy import industry_taxonomy

class RecommendationEngine:
    """Personalized recommendation engine for MSMEs"""
    
    def __init__(self):
        """Initialize the recommendation engine"""
        self.recommendation_types = [
            "legal_requirements",
            "compliance_checklist",
            "document_templates",
            "risk_assessment",
            "best_practices"
        ]
    
    def get_personalized_recommendations(self, user_id: str, recommendation_type: str = "legal_requirements") -> List[Dict[str, Any]]:
        """
        Get personalized recommendations for a user
        
        Args:
            user_id (str): User identifier
            recommendation_type (str): Type of recommendations to provide
            
        Returns:
            List[Dict[str, Any]]: List of recommendations
        """
        # Get business context
        context = context_collector.get_context_for_user(user_id)
        if not context:
            return []
        
        # Get industry insights
        insights = context_collector.get_industry_insights(user_id)
        if not insights:
            return []
        
        # Generate recommendations based on type
        if recommendation_type == "legal_requirements":
            return self._generate_legal_requirements_recommendations(context, insights)
        elif recommendation_type == "compliance_checklist":
            return self._generate_compliance_checklist(context, insights)
        elif recommendation_type == "document_templates":
            return self._generate_document_templates(context, insights)
        elif recommendation_type == "risk_assessment":
            return self._generate_risk_assessment(context, insights)
        elif recommendation_type == "best_practices":
            return self._generate_best_practices(context, insights)
        else:
            return []
    
    def _generate_legal_requirements_recommendations(self, context: Dict[str, Any], insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate legal requirements recommendations
        
        Args:
            context (Dict[str, Any]): Business context
            insights (Dict[str, Any]): Industry insights
            
        Returns:
            List[Dict[str, Any]]: Legal requirements recommendations
        """
        legal_requirements = insights.get("legal_requirements", [])
        
        recommendations = []
        for requirement in legal_requirements:
            recommendations.append({
                "type": "legal_requirement",
                "title": self._format_requirement_title(requirement),
                "description": self._get_requirement_description(requirement, context),
                "priority": self._calculate_priority(requirement, context),
                "deadline": self._estimate_deadline(requirement, context),
                "resources": self._get_requirement_resources(requirement)
            })
        
        # Sort by priority
        recommendations.sort(key=lambda x: x["priority"], reverse=True)
        
        return recommendations
    
    def _generate_compliance_checklist(self, context: Dict[str, Any], insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate compliance checklist
        
        Args:
            context (Dict[str, Any]): Business context
            insights (Dict[str, Any]): Industry insights
            
        Returns:
            List[Dict[str, Any]]: Compliance checklist
        """
        common_issues = insights.get("common_issues", [])
        
        checklist = []
        for issue in common_issues:
            checklist.append({
                "type": "compliance_item",
                "title": self._format_compliance_title(issue),
                "description": self._get_compliance_description(issue, context),
                "status": "pending",
                "due_date": self._estimate_deadline(issue, context),
                "resources": self._get_compliance_resources(issue)
            })
        
        return checklist
    
    def _generate_document_templates(self, context: Dict[str, Any], insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate document template recommendations
        
        Args:
            context (Dict[str, Any]): Business context
            insights (Dict[str, Any]): Industry insights
            
        Returns:
            List[Dict[str, Any]]: Document template recommendations
        """
        industry = context.get("industry", "")
        legal_structure = context.get("legal_structure", "")
        
        templates = [
            {
                "type": "document_template",
                "title": "Employment Agreement Template",
                "description": "Standard employment agreement for your business structure",
                "category": "employment",
                "template_type": "contract"
            },
            {
                "type": "document_template",
                "title": "Vendor Agreement Template",
                "description": "Template for agreements with suppliers and vendors",
                "category": "vendor",
                "template_type": "contract"
            },
            {
                "type": "document_template",
                "title": "Client Service Agreement",
                "description": "Standard service agreement for client engagements",
                "category": "client",
                "template_type": "contract"
            }
        ]
        
        # Add industry-specific templates
        if industry == "manufacturing":
            templates.append({
                "type": "document_template",
                "title": "Product Warranty Template",
                "description": "Standard product warranty for manufactured goods",
                "category": "product",
                "template_type": "warranty"
            })
        elif industry == "retail":
            templates.append({
                "type": "document_template",
                "title": "Customer Privacy Policy",
                "description": "Privacy policy for customer data protection",
                "category": "privacy",
                "template_type": "policy"
            })
        
        return templates
    
    def _generate_risk_assessment(self, context: Dict[str, Any], insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate risk assessment recommendations
        
        Args:
            context (Dict[str, Any]): Business context
            insights (Dict[str, Any]): Industry insights
            
        Returns:
            List[Dict[str, Any]]: Risk assessment recommendations
        """
        industry = context.get("industry", "")
        employee_count = context.get("employee_count", 0)
        
        risks = [
            {
                "type": "risk",
                "title": "Legal Compliance Risk",
                "description": "Risk of non-compliance with industry regulations",
                "severity": "high",
                "mitigation": "Regular compliance audits and legal consultations"
            },
            {
                "type": "risk",
                "title": "Contractual Risk",
                "description": "Risk of disputes in business agreements",
                "severity": "medium",
                "mitigation": "Standardized contracts and legal review process"
            }
        ]
        
        # Add employee-related risks for larger businesses
        if employee_count > 10:
            risks.append({
                "type": "risk",
                "title": "Employment Law Risk",
                "description": "Risk of employment-related legal issues",
                "severity": "high",
                "mitigation": "Clear employment policies and regular training"
            })
        
        return risks
    
    def _generate_best_practices(self, context: Dict[str, Any], insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate best practices recommendations
        
        Args:
            context (Dict[str, Any]): Business context
            insights (Dict[str, Any]): Industry insights
            
        Returns:
            List[Dict[str, Any]]: Best practices recommendations
        """
        industry = context.get("industry", "")
        
        practices = [
            {
                "type": "best_practice",
                "title": "Maintain Proper Documentation",
                "description": "Keep all legal documents organized and up-to-date",
                "category": "documentation"
            },
            {
                "type": "best_practice",
                "title": "Regular Legal Audits",
                "description": "Conduct periodic reviews of legal compliance",
                "category": "compliance"
            }
        ]
        
        # Add industry-specific best practices
        if industry == "manufacturing":
            practices.append({
                "type": "best_practice",
                "title": "Environmental Compliance",
                "description": "Ensure adherence to environmental regulations",
                "category": "environmental"
            })
        elif industry == "technology":
            practices.append({
                "type": "best_practice",
                "title": "Data Protection",
                "description": "Implement robust data security measures",
                "category": "data_security"
            })
        
        return practices
    
    def _format_requirement_title(self, requirement: str) -> str:
        """Format requirement title for display"""
        return requirement.replace("_", " ").title()
    
    def _get_requirement_description(self, requirement: str, context: Dict[str, Any]) -> str:
        """Get requirement description"""
        descriptions = {
            "factories_act": "Compliance with factory licensing and safety regulations",
            "environmental_regulations": "Adherence to environmental protection laws",
            "product_liability": "Protection against product-related legal claims",
            "consumer_protection": "Compliance with consumer rights and protection laws",
            "sales_tax": "Proper registration and payment of sales taxes",
            "data_privacy": "Protection of customer and employee personal data"
        }
        return descriptions.get(requirement, f"Compliance with {requirement.replace('_', ' ')}")
    
    def _calculate_priority(self, requirement: str, context: Dict[str, Any]) -> int:
        """Calculate priority level (1-5)"""
        # Simple priority calculation based on requirement type
        high_priority = ["factories_act", "consumer_protection", "data_privacy"]
        medium_priority = ["environmental_regulations", "sales_tax", "product_liability"]
        
        if requirement in high_priority:
            return 5
        elif requirement in medium_priority:
            return 3
        else:
            return 2
    
    def _estimate_deadline(self, item: str, context: Dict[str, Any]) -> str:
        """Estimate deadline for compliance"""
        # Simplified deadline estimation
        return "Within 30 days"
    
    def _get_requirement_resources(self, requirement: str) -> List[str]:
        """Get resources for a requirement"""
        return [f"https://legislation.gov.in/{requirement}", "Legal consultation recommended"]
    
    def _format_compliance_title(self, issue: str) -> str:
        """Format compliance title for display"""
        return issue.replace("_", " ").title()
    
    def _get_compliance_description(self, issue: str, context: Dict[str, Any]) -> str:
        """Get compliance description"""
        return f"Address {issue.replace('_', ' ')} to ensure legal compliance"
    
    def _get_compliance_resources(self, issue: str) -> List[str]:
        """Get resources for compliance"""
        return [f"https://compliance.gov.in/{issue}", "Checklist and guidelines"]

# Global instance
recommendation_engine = RecommendationEngine()