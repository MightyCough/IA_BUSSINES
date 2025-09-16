from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Configuration settings 
    for the application"""

    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI Bussines Advisor"
    VERSION: str = "1.0.0"

    # Security (AÑADE ESTAS LÍNEAS)
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    FRONTEND_URL: str = "http://localhost:5173"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173"]
    
    class Config:  # ⚠️ Cambié "config" por "Config" (mayúscula)
        env_file = ".env"

settings = Settings()