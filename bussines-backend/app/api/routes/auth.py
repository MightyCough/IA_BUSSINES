from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.schemas.user import UserCreate, UserLogin, Token, UserResponse
from app.services.user_service import user_service
from app.core.security import create_access_token, verify_token
from app.core.config import settings


router = APIRouter()
security = HTTPBearer()

@router.post("/register",response_model=Token)
def register(user_data:UserCreate):
    """
    Registrar nuevo usuario
    
    - **name**: Nombre completo del usuario
    - **email**: Email válido (será único)
    - **password**: Contraseña mínimo 6 caracteres
    """

    #Intenta crear usuario
    user = user_service.create_user(user_data)

    if not user:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "EL email ya esta registrado"
        )
    
     # Crear token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, 
        expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=user
    )

@router.post("/login",response_model=Token)
def login(user_data: UserLogin):
    """
    Iniciar sesión
    
    - **email**: Email del usuario
    - **password**: Contraseña
    """
     # Autenticar usuario
    user = user_service.authenticate_user(user_data.email, user_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos"
        )
    
    # Crear token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, 
        expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=user
    )

@router.get("/me", response_model=UserResponse)
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Obtener información del usuario actual
    Requiere token de autenticación
    """
    # Verificar token
    email = verify_token(credentials.credentials)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
    
    # Obtener usuario
    user = user_service.get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return user

@router.get("/users", response_model=list[UserResponse])
def get_all_users():
    """
    Obtener todos los usuarios (para testing)
    ⚠️ En producción esto requeriría permisos de admin
    """
    return user_service.get_all_users()

# 🎯 ENDPOINTS ADICIONALES (BONUS)

@router.delete("/users/{user_id}")
def delete_user_by_id(user_id: str):
    """
    Eliminar usuario por ID
    ⚠️ En producción requeriría permisos de admin
    """
    success = user_service.delete_user(user_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return {"message": f"Usuario {user_id} eliminado exitosamente"}

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: str):
    """
    Obtener usuario por ID
    """
    user = user_service.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return user




