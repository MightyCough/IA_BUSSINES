from pydantic_settings import BaseSettings
from typing import List
from pydantic import validator

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

    # Database
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_KEY: str

    # OpenAI
    #OPENAI_API_KEY: str = ""
    OPENROUTER_API_KEY: str = ""

    #Configuracion SMTP
    MAIL_USERNAME:str
    MAIL_PASSWORD:str
    MAIL_FROM:str
    MAIL_SERVER:str
    MAIL_PORT:int
    MAIL_STARTTLS:bool
    MAIL_SSL:bool

    # CORS
    FRONTEND_URL: str = "http://localhost:5173"
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173"
        ]
    
    # Validadores para convertir tipos
    @validator("MAIL_STARTTLS", "MAIL_SSL", pre=True)
    def parse_booleans(cls, value):
        if isinstance(value, str):
            return value.lower() in ("true", "1", "yes")
        return bool(value)

    @validator("MAIL_PORT", pre=True)
    def parse_port(cls, value):
        if isinstance(value, str):
            return int(value)
        return value

    class Config:
        env_file = ".env"

settings = Settings()