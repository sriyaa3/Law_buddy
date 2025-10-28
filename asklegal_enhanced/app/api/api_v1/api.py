from fastapi import APIRouter
from app.api.api_v1.endpoints import chat, users, documents, judgment, document_generation, msme

api_router = APIRouter()
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(judgment.router, prefix="/judgment", tags=["judgment"])
api_router.include_router(document_generation.router, prefix="/document-generation", tags=["document-generation"])
api_router.include_router(msme.router, prefix="/msme", tags=["msme"])