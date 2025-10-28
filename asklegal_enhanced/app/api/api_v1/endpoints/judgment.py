from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.judgment.predictor import judgment_predictor

router = APIRouter()

class CaseDetails(BaseModel):
    case_type: str
    facts: str
    claims: str
    evidence: str
    legal_issues: str
    jurisdiction: Optional[str] = "India"
    industry: Optional[str] = "General"

class JudgmentPrediction(BaseModel):
    probability: float
    outcome: str
    confidence: float
    explanation: str
    similar_cases: List[Dict[str, Any]]
    factors: List[str]
    error: Optional[str] = None

class JudgmentAnalysis(BaseModel):
    case_id: str
    strengths: List[str]
    weaknesses: List[str]
    legal_precedents: List[str]
    estimated_timeline: str
    cost_estimate: str

@router.post("/predict", response_model=JudgmentPrediction)
async def predict_judgment(case_details: CaseDetails):
    """
    Predict judgment outcome based on case details
    """
    try:
        # Convert Pydantic model to dictionary
        case_dict = case_details.dict()
        
        # Get prediction from judgment predictor
        prediction = judgment_predictor.predict_outcome(case_dict)
        
        # Return prediction
        return JudgmentPrediction(**prediction)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error predicting judgment: {str(e)}")

@router.post("/analyze", response_model=JudgmentAnalysis)
def analyze_case(case_details: CaseDetails):
    """Analyze case strengths and weaknesses"""
    
    # Generate analysis
    strengths = [
        "Strong documentary evidence",
        "Clear contractual terms",
        "Favorable legal precedents"
    ]
    
    weaknesses = [
        "Limited witness availability",
        "Ambiguous clause interpretation",
        "Potential statute of limitations issues"
    ]
    
    precedents = [
        "Smith v. Jones (2020) - Similar contract dispute",
        "ABC Corp v. XYZ Ltd (2019) - Breach of warranty"
    ]
    
    return JudgmentAnalysis(
        case_id="case_" + str(hash(case_details.facts))[-6:],
        strengths=strengths,
        weaknesses=weaknesses,
        legal_precedents=precedents,
        estimated_timeline="6-12 months",
        cost_estimate="₹50,000 - ₹2,00,000"
    )