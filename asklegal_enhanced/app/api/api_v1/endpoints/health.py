from fastapi import APIRouter
from typing import Dict
import sys
from pathlib import Path

router = APIRouter()

@router.get("/health")
async def health_check() -> Dict:
    """
    Health check endpoint
    Returns the status of the application and its components
    """
    # Check models
    model_path = Path("./models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf")
    models_ok = model_path.exists()
    
    # Check database
    db_path = Path("./asklegal.db")
    database_ok = db_path.exists()
    
    # Check vector store
    vector_store_path = Path("./data/legal_documents.index")
    vector_store_ok = vector_store_path.exists()
    
    # Overall status
    all_ok = models_ok and database_ok
    
    return {
        "status": "healthy" if all_ok else "degraded",
        "version": "1.0.0",
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "components": {
            "models": "ok" if models_ok else "missing",
            "database": "ok" if database_ok else "missing",
            "vector_store": "ok" if vector_store_ok else "missing"
        }
    }

@router.get("/")
async def root() -> Dict:
    """
    Root endpoint
    """
    return {
        "message": "AskLegal Enhanced API",
        "version": "1.0.0",
        "docs": "/api/v1/docs"
    }
