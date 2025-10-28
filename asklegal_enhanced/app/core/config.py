from typing import List, Union
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "AskLegal Enhanced"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    
    # Database settings - using SQLite for development
    DATABASE_URL: str = "sqlite:///./asklegal.db"
    
    # Redis settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    # Model settings
    MODEL_PATH: str = "./models"
    
    # Directory settings
    UPLOAD_DIR: str = "./uploads"
    DATA_DIR: str = "./data"
    
    class Config:
        case_sensitive = True

settings = Settings()