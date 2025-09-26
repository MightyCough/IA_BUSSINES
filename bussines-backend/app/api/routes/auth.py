from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.schemas.user import UserCreate, UserLogin, Token, UserResponse
from app.services.user_service import user_service
from app.core.security import create_access_token, verify_token
from app.core.config import settings


router = APIRouter()
security = HTTPBearer()

@router.post("/register", response_model=Token)
async def register(user_data: UserCreate):
    """
    Registrar nuevo usuario
    
    - **name**: Nombre completo del usuario
    - **email**: Email válido (será único)
    - **password**: Contraseña mínimo 6 caracteres
    """

    try:
        print(f"Registrando usuario: {user_data.email}")

        #Create user
        user = user_service.create_user(user_data)

        if not user:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "El email ya esta registrado o hay un error al crearlo"
            )

        #Create token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub":user.email},expires_delta=access_token_expires
        )

        print(f"Usuario registrado exitosamente: {user.email}")
        return {
            "access_token": access_token,  # ✅ Con doble 'S'
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "business_type": user.business_type,
                "stage": user.stage,
                "created_at": user.created_at
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en registro: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """
    Iniciar sesión
    
    - **email**: Email del usuario
    - **password**: Contraseña
    """
    try:
        print(f"API: Login attempt for {credentials.email}")

        #Autenticate user
        user = user_service.authenticate_user(credentials)

        if not user:
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Email o contraseña incorrectos"
            )
        
        #Create token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )

        print(f"✅ Login exitoso para: {user.email}")
        return {
            "access_token": access_token,  # ✅ Con doble 'S'
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "business_type": user.business_type,
                "stage": user.stage,
                "created_at": user.created_at
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
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




