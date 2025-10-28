from typing import Dict, List, Any, Optional
from pydantic import BaseModel
from datetime import datetime

class BusinessProfile(BaseModel):
    """Business profile model"""
    business_name: str
    industry: str
    subcategory: Optional[str] = None
    business_size: str  # small, medium, large
    location: str
    incorporation_date: Optional[datetime] = None
    employee_count: int = 0
    annual_revenue: Optional[float] = None
    legal_structure: str  # proprietorship, partnership, llp, pvt_ltd, ltd
    registration_number: Optional[str] = None
    tax_identification: Optional[str] = None
    contact_person: str
    contact_email: str
    contact_phone: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

class BusinessContextCollector:
    """Business context collection workflow"""
    
    def __init__(self):
        """Initialize the business context collector"""
        self.collected_profiles = {}  # In-memory storage for now
    
    def collect_business_profile(self, user_id: str, profile_data: Dict[str, Any]) -> BusinessProfile:
        """
        Collect business profile information
        
        Args:
            user_id (str): User identifier
            profile_data (Dict[str, Any]): Business profile data
            
        Returns:
            BusinessProfile: Validated business profile
        """
        # Create business profile
        profile = BusinessProfile(**profile_data)
        
        # Store profile
        self.collected_profiles[user_id] = profile
        
        return profile
    
    def get_business_profile(self, user_id: str) -> Optional[BusinessProfile]:
        """
        Get business profile for a user
        
        Args:
            user_id (str): User identifier
            
        Returns:
            Optional[BusinessProfile]: Business profile or None if not found
        """
        return self.collected_profiles.get(user_id)
    
    def update_business_profile(self, user_id: str, profile_data: Dict[str, Any]) -> Optional[BusinessProfile]:
        """
        Update business profile for a user
        
        Args:
            user_id (str): User identifier
            profile_data (Dict[str, Any]): Updated profile data
            
        Returns:
            Optional[BusinessProfile]: Updated business profile or None if not found
        """
        if user_id not in self.collected_profiles:
            return None
        
        # Get existing profile
        existing_profile = self.collected_profiles[user_id]
        
        # Update fields
        update_data = profile_data.copy()
        update_data["updated_at"] = datetime.now()
        
        # Create updated profile
        updated_profile = existing_profile.copy(update=update_data)
        
        # Store updated profile
        self.collected_profiles[user_id] = updated_profile
        
        return updated_profile
    
    def get_context_for_user(self, user_id: str) -> Dict[str, Any]:
        """
        Get business context for a user
        
        Args:
            user_id (str): User identifier
            
        Returns:
            Dict[str, Any]: Business context information
        """
        profile = self.get_business_profile(user_id)
        if not profile:
            return {}
        
        context = {
            "business_name": profile.business_name,
            "industry": profile.industry,
            "subcategory": profile.subcategory,
            "business_size": profile.business_size,
            "location": profile.location,
            "legal_structure": profile.legal_structure,
            "employee_count": profile.employee_count,
            "annual_revenue": profile.annual_revenue
        }
        
        return context
    
    def get_industry_insights(self, user_id: str) -> Dict[str, List[str]]:
        """
        Get industry-specific insights for a user
        
        Args:
            user_id (str): User identifier
            
        Returns:
            Dict[str, List[str]]: Industry insights including legal requirements and common issues
        """
        from app.msme.knowledge_base.industry_taxonomy import industry_taxonomy
        
        profile = self.get_business_profile(user_id)
        if not profile:
            return {}
        
        # Get industry information
        industry_info = industry_taxonomy.get_industry_info(profile.industry)
        
        insights = {
            "legal_requirements": industry_info.get("legal_requirements", []),
            "common_issues": industry_info.get("common_issues", []),
            "industry_name": industry_info.get("name", ""),
            "industry_description": industry_info.get("description", "")
        }
        
        return insights

# Global instance
context_collector = BusinessContextCollector()