from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.schemas.user import UserCreate, UserLogin, Token, UserResponse,UserVerification,UserResendCode,RegisterInitResponse,RegisterVerifyResponse
from app.services.user_service import user_service
from app.core.security import create_access_token, verify_token
from app.core.config import settings
from app.services.email_service import email_service

router = APIRouter()
security = HTTPBearer()

@router.post("/request-register", response_model=RegisterInitResponse)
async def request_register(user_data: UserCreate):
    """
    Paso 1: Usuario solicita registro.
    No se crea en la BD todavía, solo se envía el código de verificación.
    """
    # Verificar si ya existe en la BD
    existing = user_service.get_user_by_email(user_data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )

    # Generar y enviar código
    code = await email_service.send_verification_email(user_data.email, user_data.full_name)

    # Guardar los datos en memoria temporal
    email_service.verification_codes[user_data.email] = {
        "code": code,
        "user_data": user_data.model_dump(),
        "expires_at": datetime.now() + timedelta(minutes=5)
    }

    return {
        "message": "Se envió un código de verificación a tu correo",
        "redirect_url": "/register/verification",
        "email": user_data.email
    }
    
@router.post("/register/verify", response_model=RegisterVerifyResponse)
async def verify_register(data: UserVerification):
    """
    Paso 2: Verificar el código y crear el usuario en la BD.
    """
    print("📥 Email recibido en verify_register:", data.email)
    print("📥 Código recibido en verify_register:", data.verification_code)
    print("📦 Codes en memoria:", email_service.verification_codes)

    # 1. Verificar código
    if not email_service.verify_code(data.email, data.verification_code):
        raise HTTPException(status_code=400, detail="Código inválido o expirado")

    # 2. Recuperar datos temporales
    temp = email_service.verification_codes.get(data.email)
    if not temp:
        raise HTTPException(status_code=400, detail="No hay datos de registro en espera")

    user_data = UserCreate(**temp["user_data"])

    # 3. Crear usuario en BD
    user = user_service.create_user(user_data)
    if not user:
        raise HTTPException(status_code=500, detail="Error al crear el usuario en BD")

    # 4. Limpiar código SOLO AHORA ✅
    email_service.cleanup_code(data.email)

    # 5. Generar token
    access_token = create_access_token(data={"sub": user.email})

    return {
        "message": "Usuario registrado y verificado exitosamente",
        "user": user,
        "access_token": access_token,
        "token_type": "bearer"
    }



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
        
        #Verifica si el usuario esta verificado
        if not user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Debes verificar tu correo antes de iniciar sesion"
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

@router.post("/verify-email")
def verify_email(data: UserVerification):
    """"
    Verificar el codigo enviado por email y activa el usuario"""
    if email_service.verify_code(data.email,data.verification_code):
        user_service.set_user_verified(data.email)
        return{"message":"Email verificado exitosamente"}
    else:
        raise HTTPException(status_code=400,detail="codigo invalido o expirado")
    
@router.post("/resend-code")
async def resend_code(data:UserResendCode):
    """
    Reenviar el codigo de verificacion al email del usuario"""
    user = user_service.get_user_by_email(data.email)
    if not user:
        raise HTTPException(status_code=404,detail="Usuario no encontrado")
    await user_service.resend_verification_email(data.email,user.full_name)
    return {"message":"Codigo reenviado"}

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




