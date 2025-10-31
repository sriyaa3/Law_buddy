from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional
import os
import uuid
from app.documents.generator import document_generator
from app.core.config import settings

router = APIRouter()

class DocumentRequest(BaseModel):
    template_type: str
    details: Dict[str, Any]
    filename: Optional[str] = None

class DocumentResponse(BaseModel):
    document_id: str
    filename: str
    message: str
    download_url: str

@router.post("/generate", response_model=DocumentResponse)
async def generate_document(request: DocumentRequest):
    """
    Generate legal document from template
    """
    try:
        # Generate unique filename if not provided
        if not request.filename:
            timestamp = uuid.uuid4().hex[:8]
            request.filename = f"{request.template_type}_{timestamp}.docx"
        
        # Create output path
        output_dir = os.path.join(settings.DATA_DIR, "generated_documents")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, request.filename)
        
        # Generate document
        success = document_generator.generate_document(
            request.template_type, 
            request.details, 
            output_path
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to generate document")
        
        # Return response
        document_id = uuid.uuid4().hex
        download_url = f"/api/v1/documents/generated/{document_id}"
        
        return DocumentResponse(
            document_id=document_id,
            filename=request.filename,
            message="Document generated successfully",
            download_url=download_url
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating document: {str(e)}")

@router.get("/templates")
async def get_templates():
    """
    Get available document templates
    """
    try:
        # Get template information from document generator
        template_info = {
            "nda": {
                "title": "Non-Disclosure Agreement",
                "description": "Create a legally binding NDA for protecting confidential information",
                "fields": ["disclosing_party", "receiving_party", "effective_date", "term"]
            },
            "employment_contract": {
                "title": "Employment Contract",
                "description": "Generate a comprehensive employment agreement",
                "fields": ["employer", "employee", "position", "salary", "start_date", "effective_date"]
            },
            "service_agreement": {
                "title": "Service Agreement",
                "description": "Create a service agreement for business relationships",
                "fields": ["client", "service_provider", "services", "payment_terms", "term", "effective_date"]
            },
            "loan_agreement": {
                "title": "Loan Agreement",
                "description": "Generate a loan agreement between parties",
                "fields": ["lender", "borrower", "loan_amount", "interest_rate", "repayment_terms", "effective_date"]
            },
            "notice": {
                "title": "Legal Notice",
                "description": "Create a formal legal notice",
                "fields": ["to_party", "from_party", "subject", "notice_content", "notice_date", "required_action", "response_deadline", "contact_info"]
            }
        }
        
        return JSONResponse(content={"templates": template_info})
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving templates: {str(e)}")

@router.get("/generated/{document_id}")
async def download_document(document_id: str):
    """
    Download generated document
    """
    try:
        # In a real implementation, you would map document_id to actual file paths
        # For now, we'll just return a placeholder
        output_dir = os.path.join(settings.DATA_DIR, "generated_documents")
        
        # Find the most recent document (simplified approach)
        if os.path.exists(output_dir):
            files = os.listdir(output_dir)
            if files:
                latest_file = max(files, key=lambda f: os.path.getctime(os.path.join(output_dir, f)))
                file_path = os.path.join(output_dir, latest_file)
                
                if os.path.exists(file_path):
                    return FileResponse(
                        file_path, 
                        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                        filename=latest_file
                    )
        
        raise HTTPException(status_code=404, detail="Document not found")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading document: {str(e)}")
