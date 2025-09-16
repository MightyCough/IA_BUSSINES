from pydantic import BaseModel, EmailStr, validator
from typing import Optional

class UserBase(BaseModel):
    """Propiedades base del usuario"""
    email: EmailStr
    name: str

class UserCreate(UserBase):
    """Esquema para crear usuario"""
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('La contraseña debe tener al menos 6 caracteres')
        return v
    
    @validator('name')
    def validate_name(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('El nombre debe tener al menos 2 caracteres')
        return v.strip()
    
    @validator('email')
    def remove_spaces_email(cls, v):
        return v.strip()

class UserUpdate(UserBase):
    """Esquema para actualizar nombre"""
    name: Optional[str] = None

    @validator('name')
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
    created_at: str
    
class Token(BaseModel):
    """Esquema para token de acceso"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

