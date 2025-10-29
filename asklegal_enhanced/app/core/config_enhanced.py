"""
Enhanced Configuration for AI Law Buddy
Includes support for Phi-3, Mistral, Neo4j, Upstash Redis, and Privacy Settings
"""

from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Application Settings
    PROJECT_NAME: str = "AI Law Buddy - Empowering MSMEs with Legal Compliance"
    API_V1_STR: str = "/api/v1"
    APP_PORT: int = Field(default=8001, env="APP_PORT")
    SECRET_KEY: str = Field(default="change-in-production", env="SECRET_KEY")
    DEBUG: bool = Field(default=False)
    
    # Google Gemini (Fallback)
    GOOGLE_API_KEY: Optional[str] = Field(default=None, env="GOOGLE_API_KEY")
    
    # Upstash Redis Configuration
    UPSTASH_REDIS_URL: Optional[str] = Field(default=None, env="UPSTASH_REDIS_URL")
    UPSTASH_REDIS_TOKEN: Optional[str] = Field(default=None, env="UPSTASH_REDIS_TOKEN")
    
    # Local Redis (Fallback)
    REDIS_HOST: str = Field(default="localhost", env="REDIS_HOST")
    REDIS_PORT: int = Field(default=6379, env="REDIS_PORT")
    REDIS_DB: int = Field(default=0, env="REDIS_DB")
    
    # Neo4j Graph Database
    NEO4J_URI: str = Field(default="bolt://localhost:7687", env="NEO4J_URI")
    NEO4J_USER: str = Field(default="neo4j", env="NEO4J_USER")
    NEO4J_PASSWORD: str = Field(default="password", env="NEO4J_PASSWORD")
    NEO4J_DATABASE: str = Field(default="neo4j", env="NEO4J_DATABASE")
    
    # Tesseract OCR
    TESSERACT_CMD: str = Field(default="/usr/bin/tesseract", env="TESSERACT_CMD")
    
    # Model Paths
    MODEL_DIR: str = Field(default="./models", env="MODEL_DIR")
    PHI3_MODEL_PATH: str = Field(
        default="./models/phi-3-mini-4k-instruct-q4.gguf", 
        env="PHI3_MODEL_PATH"
    )
    MISTRAL_MODEL_PATH: str = Field(
        default="./models/mistral-7b-instruct-v0.2.Q4_K_M.gguf", 
        env="MISTRAL_MODEL_PATH"
    )
    LAYOUTLM_MODEL: str = Field(
        default="microsoft/layoutlmv3-base", 
        env="LAYOUTLM_MODEL"
    )
    LEGAL_BERT_MODEL: str = Field(
        default="law-ai/InLegalBERT", 
        env="LEGAL_BERT_MODEL"
    )
    
    # Directory Settings
    UPLOAD_FOLDER: str = Field(default="./uploads", env="UPLOAD_FOLDER")
    DATA_DIR: str = Field(default="./data", env="DATA_DIR")
    VECTOR_DB_PATH: str = Field(default="./data/vector_db", env="VECTOR_DB_PATH")
    LEGAL_DATA_PATH: str = Field(default="./data/legal_documents", env="LEGAL_DATA_PATH")
    TEMPLATE_DIR: str = Field(default="./templates", env="TEMPLATE_DIR")
    
    # Upload Settings
    MAX_UPLOAD_SIZE: int = Field(default=16777216, env="MAX_UPLOAD_SIZE")  # 16MB
    ALLOWED_EXTENSIONS: set = {"pdf", "docx", "doc", "txt", "png", "jpg", "jpeg"}
    
    # Privacy Settings
    ENABLE_DIFFERENTIAL_PRIVACY: bool = Field(default=True, env="ENABLE_DIFFERENTIAL_PRIVACY")
    PRIVACY_EPSILON: float = Field(default=1.0, env="PRIVACY_EPSILON")
    PRIVACY_DELTA: float = Field(default=1e-5, env="PRIVACY_DELTA")
    SENSITIVITY_THRESHOLD: float = Field(default=0.7)
    
    # Performance Settings
    MAX_WORKERS: int = Field(default=4, env="MAX_WORKERS")
    CACHE_SIZE: int = Field(default=1000, env="CACHE_SIZE")
    MAX_CONTEXT_LENGTH: int = Field(default=4096)
    BATCH_SIZE: int = Field(default=8)
    
    # Retrieval Settings
    TOP_K_RETRIEVAL: int = Field(default=5)
    SIMILARITY_THRESHOLD: float = Field(default=0.75)
    HYBRID_ALPHA: float = Field(default=0.5)  # Balance between BM25 and vector search
    
    # Model Inference Settings
    TEMPERATURE: float = Field(default=0.7)
    MAX_TOKENS: int = Field(default=512)
    TOP_P: float = Field(default=0.9)
    
    # Database
    DATABASE_URL: str = Field(default="sqlite:///./ai_law_buddy.db", env="DATABASE_URL")
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create global settings instance
settings = Settings()

# Create necessary directories
os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(settings.DATA_DIR, exist_ok=True)
os.makedirs(settings.VECTOR_DB_PATH, exist_ok=True)
os.makedirs(settings.MODEL_DIR, exist_ok=True)
