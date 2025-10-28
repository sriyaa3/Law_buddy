from typing import Dict, Any, List
from app.retrieval.hybrid_retriever import hybrid_retriever
from app.slm.model_router import model_router
from app.document_processing.embedders import text_embedder
import numpy as np

class JudgmentPredictor:
    """Judgment predictor that analyzes case details and predicts outcomes"""
    
    def __init__(self):
        self.hybrid_retriever = hybrid_retriever
        self.model_router = model_router
        self.text_embedder = text_embedder
    
    def predict_outcome(self, case_details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict case outcome based on details
        
        Args:
            case_details (Dict[str, Any]): Case details
            
        Returns:
            Dict[str, Any]: Prediction results with probability and explanation
        """
        try:
            # Extract key information
            case_type = case_details.get("case_type", "civil")
            facts = case_details.get("facts", "")
            claims = case_details.get("claims", "")
            evidence = case_details.get("evidence", "")
            legal_issues = case_details.get("legal_issues", "")
            
            # Create comprehensive case description
            case_description = f"""
Case Type: {case_type}
Facts: {facts}
Claims: {claims}
Evidence: {evidence}
Legal Issues: {legal_issues}
"""
            
            # Retrieve similar cases
            similar_cases = self._find_similar_cases(case_description, limit=5)
            
            # Analyze similar cases to predict outcome
            prediction = self._analyze_similar_cases(case_description, similar_cases)
            
            # Generate explanation using model router
            explanation = self._generate_explanation(case_description, similar_cases, prediction)
            
            return {
                "probability": prediction["probability"],
                "outcome": prediction["outcome"],
                "confidence": prediction["confidence"],
                "explanation": explanation,
                "similar_cases": similar_cases,
                "factors": prediction["factors"]
            }
            
        except Exception as e:
            return {
                "error": f"Error predicting outcome: {e}",
                "probability": 0.0,
                "outcome": "unknown",
                "confidence": 0.0
            }
    
    def _find_similar_cases(self, case_description: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Find similar cases using hybrid retrieval
        
        Args:
            case_description (str): Case description
            limit (int): Maximum number of similar cases
            
        Returns:
            List[Dict[str, Any]]: Similar cases
        """
        try:
            # Use hybrid retriever to find similar cases
            results = self.hybrid_retriever.retrieve(case_description, limit=limit)
            return results
        except Exception as e:
            print(f"Error finding similar cases: {e}")
            return []
    
    def _analyze_similar_cases(self, case_description: str, similar_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze similar cases to predict outcome
        
        Args:
            case_description (str): Current case description
            similar_cases (List[Dict[str, Any]]): Similar cases
            
        Returns:
            Dict[str, Any]: Prediction analysis
        """
        if not similar_cases:
            return {
                "probability": 0.5,
                "outcome": "uncertain",
                "confidence": 0.1,
                "factors": ["No similar cases found"]
            }
        
        # Simple analysis based on similar case outcomes
        favorable_outcomes = 0
        total_cases = len(similar_cases)
        factors = []
        
        for case in similar_cases:
            # Extract outcome from case content (simplified)
            content = case["content"].lower()
            if "favorable" in content or "granted" in content or "successful" in content:
                favorable_outcomes += 1
                factors.append(f"Similar case outcome: favorable (score: {case['score']:.2f})")
            elif "unfavorable" in content or "denied" in content or "dismissed" in content:
                factors.append(f"Similar case outcome: unfavorable (score: {case['score']:.2f})")
            else:
                factors.append(f"Similar case outcome: mixed (score: {case['score']:.2f})")
        
        # Calculate probability
        probability = favorable_outcomes / total_cases if total_cases > 0 else 0.5
        confidence = min(total_cases / 5.0, 1.0)  # Confidence based on number of similar cases
        
        # Determine outcome
        if probability > 0.7:
            outcome = "favorable"
        elif probability < 0.3:
            outcome = "unfavorable"
        else:
            outcome = "uncertain"
        
        return {
            "probability": probability,
            "outcome": outcome,
            "confidence": confidence,
            "factors": factors
        }
    
    def _generate_explanation(self, case_description: str, similar_cases: List[Dict[str, Any]], prediction: Dict[str, Any]) -> str:
        """
        Generate explanation for prediction
        
        Args:
            case_description (str): Current case description
            similar_cases (List[Dict[str, Any]]): Similar cases
            prediction (Dict[str, Any]): Prediction analysis
            
        Returns:
            str: Explanation
        """
        prompt = f"""
You are a legal expert AI assistant. Analyze the following case and provide an explanation for the predicted outcome.

Current Case:
{case_description}

Prediction Analysis:
- Probability: {prediction['probability']:.2f}
- Outcome: {prediction['outcome']}
- Confidence: {prediction['confidence']:.2f}

Similar Cases Found: {len(similar_cases)}

Please provide a detailed explanation of the prediction, including:
1. Key factors influencing the outcome
2. How similar cases inform this prediction
3. Potential legal precedents
4. Areas of uncertainty
5. Recommendations for strengthening the case

Keep the explanation professional and focused on legal reasoning.
"""
        
        try:
            explanation = self.model_router.generate_response(
                "Explain this legal case prediction", 
                prompt,
                model_preference=None  # Let router decide
            )
            return explanation
        except Exception as e:
            return f"Error generating explanation: {e}"

# Global instance
judgment_predictor = JudgmentPredictor()