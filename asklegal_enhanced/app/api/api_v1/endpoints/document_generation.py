from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional
import os
import uuid
import json
from app.documents.generator import document_generator
from app.core.config import settings

router = APIRouter()

# Persistent storage file for document mappings
STORAGE_FILE = os.path.join(settings.DATA_DIR, "document_mappings.json")

def load_document_storage() -> Dict[str, str]:
    """Load document storage from file"""
    if os.path.exists(STORAGE_FILE):
        try:
            with open(STORAGE_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_document_storage(storage: Dict[str, str]):
    """Save document storage to file"""
    os.makedirs(os.path.dirname(STORAGE_FILE), exist_ok=True)
    with open(STORAGE_FILE, 'w') as f:
        json.dump(storage, f)

# Load existing mappings
document_storage: Dict[str, str] = load_document_storage()

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
        # Generate unique document ID
        document_id = uuid.uuid4().hex
        
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
        
        # Store mapping and persist to file
        document_storage[document_id] = output_path
        save_document_storage(document_storage)
        
        # Return response with proper download URL
        download_url = f"/api/v1/document-generation/generated/{document_id}"
        
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
    Download generated document by ID
    """
    try:
        # Check if document exists in storage
        if document_id not in document_storage:
            raise HTTPException(status_code=404, detail="Document not found")
        
        file_path = document_storage[document_id]
        
        # Check if file exists on disk
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Document file not found")
        
        # Get filename
        filename = os.path.basename(file_path)
        
        # Return file with proper headers for download
        return FileResponse(
            file_path, 
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            filename=filename,
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Access-Control-Expose-Headers": "Content-Disposition"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading document: {str(e)}")

@router.get("/list")
async def list_documents():
    """
    List all generated documents
    """
    try:
        output_dir = os.path.join(settings.DATA_DIR, "generated_documents")
        
        if not os.path.exists(output_dir):
            return JSONResponse(content={"documents": []})
        
        documents = []
        for doc_id, file_path in document_storage.items():
            if os.path.exists(file_path):
                filename = os.path.basename(file_path)
                file_size = os.path.getsize(file_path)
                documents.append({
                    "document_id": doc_id,
                    "filename": filename,
                    "size": file_size,
                    "download_url": f"/api/v1/document-generation/generated/{doc_id}"
                })
        
        return JSONResponse(content={"documents": documents})
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing documents: {str(e)}")