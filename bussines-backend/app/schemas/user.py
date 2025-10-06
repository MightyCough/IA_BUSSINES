from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Propiedades base del usuario"""
    email: EmailStr

class UserCreate(UserBase):
    """Esquema para crear usuario"""
    password: str
    full_name: str
    business_type: Optional[str] = "producto"
    stage: Optional[str] = "idea"

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('La contraseña debe tener al menos 6 caracteres')
        return v
    
    @validator('full_name')
    def validate_name(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('El nombre debe tener al menos 2 caracteres')
        return v.strip()
    
    @validator('email')
    def remove_spaces_email(cls, v):
        return v.strip()


class UserUpdate(UserBase):
    """Esquema para actualizar nombre"""
    full_name: Optional[str] = None

    @validator('full_name')
    def validate_name(cls, v):
        if v and len(v.strip()) < 2:
            raise ValueError('El nombre debe tener al menos 2 caracteres')
        return v.strip() if v else v

class UserLogin(BaseModel):
    """Esquema para login"""
    email: EmailStr
    password: str

class UserResponse(UserBase):
    """Esquema para respuesta (sin password)"""
    id: str
    full_name: str
    business_type: str
    stage: str
    created_at: Optional[datetime] = None
    is_verified: Optional[bool] = False

    class Config:
        from_attributes = True
    
class Token(BaseModel):
    """Esquema para token de acceso"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class RegisterInitResponse(BaseModel):
    """Respuesta al iniciar el registro (envío de código)"""
    message: str
    redirect_url: str
    email: EmailStr

class RegisterVerifyResponse(BaseModel):
    """Respuesta al verificar el código (usuario creado y autenticado)"""
    message: str
    user: UserResponse
    access_token: Optional[str] = None
    token_type: Optional[str] = "bearer"


class UserVerification(BaseModel):
    email: EmailStr
    verification_code:str

    @validator("email")
    def normalize_email(cls,v):
        return v.strip().lower()

class UserResendCode(BaseModel):
    email: EmailStr

