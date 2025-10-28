from typing import Dict, List, Any

class IndustryTaxonomy:
    """Industry taxonomy for MSME legal requirements"""
    
    def __init__(self):
        """Initialize the industry taxonomy"""
        self.industries = self._load_industry_taxonomy()
    
    def _load_industry_taxonomy(self) -> Dict[str, Dict[str, Any]]:
        """
        Load industry taxonomy with legal requirements
        
        Returns:
            Dict[str, Dict[str, Any]]: Industry taxonomy
        """
        return {
            "manufacturing": {
                "name": "Manufacturing",
                "description": "Production of goods from raw materials",
                "subcategories": [
                    "food_processing",
                    "textiles",
                    "electronics",
                    "machinery",
                    "chemicals"
                ],
                "legal_requirements": [
                    "factories_act",
                    "environmental_regulations",
                    "product_liability",
                    "quality_standards",
                    "worker_safety"
                ],
                "common_issues": [
                    "factory_licensing",
                    "environmental_compliance",
                    "product_defects",
                    "supply_chain_disputes"
                ]
            },
            "retail": {
                "name": "Retail",
                "description": "Sale of goods to consumers",
                "subcategories": [
                    "clothing",
                    "electronics",
                    "grocery",
                    "furniture",
                    "automotive"
                ],
                "legal_requirements": [
                    "consumer_protection",
                    "sales_tax",
                    "product_warranties",
                    "shop_establishment_act",
                    "data_privacy"
                ],
                "common_issues": [
                    "consumer_complaints",
                    "supplier_agreements",
                    "tax_compliance",
                    "inventory_management"
                ]
            },
            "services": {
                "name": "Services",
                "description": "Provision of services to clients",
                "subcategories": [
                    "consulting",
                    "healthcare",
                    "education",
                    "hospitality",
                    "transportation"
                ],
                "legal_requirements": [
                    "service_contracts",
                    "professional_liability",
                    "data_protection",
                    "employment_law",
                    "industry_regulations"
                ],
                "common_issues": [
                    "client_disputes",
                    "service_level_agreements",
                    "employee_contracts",
                    "regulatory_compliance"
                ]
            },
            "technology": {
                "name": "Technology",
                "description": "Software development and IT services",
                "subcategories": [
                    "software_development",
                    "web_services",
                    "mobile_apps",
                    "cybersecurity",
                    "data_analytics"
                ],
                "legal_requirements": [
                    "intellectual_property",
                    "data_privacy",
                    "software_licensing",
                    "cybersecurity_law",
                    "export_controls"
                ],
                "common_issues": [
                    "ip_infringement",
                    "data_breaches",
                    "software_licensing",
                    "client_contracts"
                ]
            },
            "healthcare": {
                "name": "Healthcare",
                "description": "Medical services and healthcare products",
                "subcategories": [
                    "clinics",
                    "pharmacies",
                    "medical_devices",
                    "telemedicine",
                    "wellness"
                ],
                "legal_requirements": [
                    "medical_council_regulations",
                    "drug_control_act",
                    "patient_privacy",
                    "medical_negligence",
                    "healthcare_standards"
                ],
                "common_issues": [
                    "medical_malpractice",
                    "drug_regulatory_compliance",
                    "patient_confidentiality",
                    "insurance_claims"
                ]
            }
        }
    
    def get_industries(self) -> List[str]:
        """
        Get list of industries
        
        Returns:
            List[str]: List of industry identifiers
        """
        return list(self.industries.keys())
    
    def get_industry_info(self, industry_id: str) -> Dict[str, Any]:
        """
        Get information about a specific industry
        
        Args:
            industry_id (str): Industry identifier
            
        Returns:
            Dict[str, Any]: Industry information
        """
        return self.industries.get(industry_id, {})
    
    def get_legal_requirements(self, industry_id: str) -> List[str]:
        """
        Get legal requirements for an industry
        
        Args:
            industry_id (str): Industry identifier
            
        Returns:
            List[str]: Legal requirements
        """
        industry = self.industries.get(industry_id, {})
        return industry.get("legal_requirements", [])
    
    def get_common_issues(self, industry_id: str) -> List[str]:
        """
        Get common legal issues for an industry
        
        Args:
            industry_id (str): Industry identifier
            
        Returns:
            List[str]: Common legal issues
        """
        industry = self.industries.get(industry_id, {})
        return industry.get("common_issues", [])
    
    def find_industry_by_keywords(self, keywords: List[str]) -> List[str]:
        """
        Find industries based on keywords
        
        Args:
            keywords (List[str]): Keywords to search for
            
        Returns:
            List[str]: Matching industry identifiers
        """
        matching_industries = []
        keywords_lower = [kw.lower() for kw in keywords]
        
        for industry_id, industry_info in self.industries.items():
            # Check industry name and description
            name = industry_info.get("name", "").lower()
            description = industry_info.get("description", "").lower()
            
            # Check subcategories
            subcategories = industry_info.get("subcategories", [])
            subcategories_lower = [sc.lower() for sc in subcategories]
            
            # Match keywords
            if any(kw in name or kw in description or kw in subcategories_lower for kw in keywords_lower):
                matching_industries.append(industry_id)
        
        return matching_industries

# Global instance
industry_taxonomy = IndustryTaxonomy()