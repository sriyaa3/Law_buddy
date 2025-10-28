from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Optional
import random

router = APIRouter()

class BusinessProfile(BaseModel):
    business_name: str
    industry: str
    size: str  # small, medium, large
    location: str
    employee_count: int
    annual_revenue: float

class ComplianceRequirement(BaseModel):
    id: str
    title: str
    description: str
    deadline: str
    priority: str  # high, medium, low
    status: str  # pending, completed, overdue
    category: str  # tax, labor, licensing, etc.

class Recommendation(BaseModel):
    id: str
    title: str
    description: str
    priority: str
    category: str
    action_required: bool

class RiskAssessment(BaseModel):
    id: str
    title: str
    description: str
    severity: str  # high, medium, low
    mitigation: str

INDUSTRY_REQUIREMENTS = {
    "manufacturing": [
        "Factory License Registration",
        "Pollution Control Board Compliance",
        "GST Registration",
        "Shops & Establishments Act Registration",
        "Professional Tax Registration",
        "Employee Provident Fund Registration",
        "Employee State Insurance Registration"
    ],
    "retail": [
        "GST Registration",
        "Shops & Establishments Act Registration",
        "Professional Tax Registration",
        "Food License (FSSAI) - if applicable",
        "Import Export Code - if applicable"
    ],
    "services": [
        "GST Registration",
        "Professional Tax Registration",
        "Service Tax Registration - if applicable",
        "Shops & Establishments Act Registration"
    ],
    "technology": [
        "GST Registration",
        "Professional Tax Registration",
        "Shops & Establishments Act Registration",
        "Import Export Code - if applicable",
        "Startup India Registration - if applicable"
    ]
}

@router.post("/profile")
def create_business_profile(profile: BusinessProfile):
    """Create or update business profile"""
    return {
        "message": "Business profile created successfully",
        "profile_id": f"profile_{hash(profile.business_name) % 10000}",
        "industry": profile.industry
    }

@router.get("/compliance/{industry}")
def get_compliance_requirements(industry: str):
    """Get compliance requirements for specific industry"""
    requirements = INDUSTRY_REQUIREMENTS.get(industry.lower(), [])
    
    compliance_list = []
    for i, req in enumerate(requirements):
        compliance_list.append(ComplianceRequirement(
            id=f"req_{i+1}",
            title=req,
            description=f"Compliance requirement for {req}",
            deadline="2025-12-31",
            priority=random.choice(["high", "medium", "low"]),
            status=random.choice(["pending", "completed"]),
            category=random.choice(["tax", "labor", "licensing", "miscellaneous"])
        ))
    
    return {"requirements": compliance_list}

@router.get("/recommendations/{industry}")
def get_recommendations(industry: str):
    """Get recommendations for specific industry"""
    base_recommendations = [
        {
            "title": "Review Employment Contracts",
            "description": "Ensure all employee contracts are up-to-date and compliant with labor laws",
            "priority": "high",
            "category": "HR"
        },
        {
            "title": "Update Privacy Policy",
            "description": "Review and update privacy policy to comply with data protection regulations",
            "priority": "medium",
            "category": "Compliance"
        },
        {
            "title": "Conduct Legal Audit",
            "description": "Perform annual legal audit to identify potential risks and compliance gaps",
            "priority": "medium",
            "category": "Risk Management"
        }
    ]
    
    industry_specific = {
        "manufacturing": [
            {
                "title": "Environmental Compliance Check",
                "description": "Verify compliance with pollution control regulations",
                "priority": "high",
                "category": "Environmental"
            }
        ],
        "retail": [
            {
                "title": "Consumer Protection Review",
                "description": "Ensure compliance with consumer protection laws",
                "priority": "medium",
                "category": "Compliance"
            }
        ],
        "technology": [
            {
                "title": "IP Portfolio Review",
                "description": "Audit intellectual property portfolio and ensure proper protection",
                "priority": "high",
                "category": "IP"
            }
        ]
    }
    
    all_recommendations = base_recommendations + industry_specific.get(industry.lower(), [])
    
    recommendation_list = []
    for i, rec in enumerate(all_recommendations):
        recommendation_list.append(Recommendation(
            id=f"rec_{i+1}",
            title=rec["title"],
            description=rec["description"],
            priority=rec["priority"],
            category=rec["category"],
            action_required=True
        ))
    
    return {"recommendations": recommendation_list}

@router.get("/risks/{industry}")
def get_risk_assessment(industry: str):
    """Get risk assessment for specific industry"""
    base_risks = [
        {
            "title": "Contract Disputes",
            "description": "Risk of disputes arising from unclear contract terms",
            "severity": "medium",
            "mitigation": "Implement standardized contracts with clear terms and regular legal review"
        },
        {
            "title": "Employment Law Violations",
            "description": "Risk of non-compliance with labor laws and regulations",
            "severity": "high",
            "mitigation": "Regular training for HR personnel and periodic legal audits"
        }
    ]
    
    industry_specific = {
        "manufacturing": [
            {
                "title": "Environmental Liability",
                "description": "Risk of environmental violations and associated penalties",
                "severity": "high",
                "mitigation": "Regular environmental audits and compliance monitoring"
            }
        ],
        "retail": [
            {
                "title": "Product Liability",
                "description": "Risk of claims related to product defects or safety issues",
                "severity": "medium",
                "mitigation": "Implement quality control measures and product testing protocols"
            }
        ],
        "technology": [
            {
                "title": "Data Breach",
                "description": "Risk of cybersecurity incidents and data protection violations",
                "severity": "high",
                "mitigation": "Implement robust cybersecurity measures and regular security audits"
            }
        ]
    }
    
    all_risks = base_risks + industry_specific.get(industry.lower(), [])
    
    risk_list = []
    for i, risk in enumerate(all_risks):
        risk_list.append(RiskAssessment(
            id=f"risk_{i+1}",
            title=risk["title"],
            description=risk["description"],
            severity=risk["severity"],
            mitigation=risk["mitigation"]
        ))
    
    return {"risks": risk_list}

@router.get("/checklist/{industry}")
def get_compliance_checklist(industry: str):
    """Get compliance checklist for specific industry"""
    requirements = INDUSTRY_REQUIREMENTS.get(industry.lower(), [])
    
    checklist = []
    for i, req in enumerate(requirements):
        checklist.append({
            "id": f"item_{i+1}",
            "title": req,
            "completed": random.choice([True, False]),
            "due_date": "2025-12-31",
            "priority": random.choice(["high", "medium", "low"])
        })
    
    return {"checklist": checklist}