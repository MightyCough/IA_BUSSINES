from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes import auth

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API para asesor de negocios con IA - Sistema de autenticación",
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas de autenticación
app.include_router(
    auth.router, 
    prefix=f"{settings.API_V1_STR}/auth", 
    tags=["Authentication"]
)

@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy", 
        "service": settings.PROJECT_NAME,
        "users_count": len(auth.user_service.get_all_users())
    }

@app.get("/api/info")
def api_info():
    """Información de la API"""
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "endpoints": {
            "auth": f"{settings.API_V1_STR}/auth",
            "docs": "/docs",
            "health": "/health"
        },
        "features": [
            "User Registration",
            "User Login", 
            "JWT Authentication",
            "Password Hashing",
            "CORS Enabled"
        ]
    }