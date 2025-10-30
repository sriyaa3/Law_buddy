from typing import List, Union
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "AskLegal Enhanced"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    BACKEND_CORS_ORIGINS: List[str] = ["*"]  # Allow all origins for development
    
    # Database settings - using SQLite for development
    DATABASE_URL: str = "sqlite:///./asklegal.db"
    
    # Redis settings (optional for development)
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    # Model settings
    MODEL_PATH: str = "./models"
    
    # Hugging Face API settings
    HUGGINGFACE_API_KEY: str = os.getenv("HUGGINGFACE_API_KEY", "")  # Optional, free tier works without key
    HUGGINGFACE_MODEL: str = "mistralai/Mistral-7B-Instruct-v0.2"  # Free model for inference
    
    # Directory settings
    UPLOAD_DIR: str = "./uploads"
    DATA_DIR: str = "./data"
    
    class Config:
        case_sensitive = True

settings = Settings()
