from typing import Optional, Dict, List
from datetime import datetime
from app.schemas.user import UserCreate, UserResponse, UserUpdate,UserLogin
from app.core.security import get_password_hash, verify_password
from app.core.database import supabase_db
from app.services.email_service import email_service
import asyncio
class UserService:    
    def __init__(self):
        self.db = supabase_db.get_client()

    def create_user(self, user_data: UserCreate) -> Optional[UserResponse]:
        """"Crear Nuevo Usuario"""
        try: 
            print(f"Creando usuario: {user_data.email}")

            #Verify if exists
            existing = self.db.table('users').select('email').eq('email',user_data.email).execute()
            if existing.data:
                print(f"Usuario ya existe: {user_data.email}")
                return None
            
            #Creat a new user
            new_user={
                "email":user_data.email,
                "password_hash":get_password_hash(user_data.password),
                "is_verified": False
            }

            user_result = self.db.table('users').insert(new_user).execute()
            print(f"Usuario creado en tabla users: {user_result.data}")

            if not user_result.data:
                print(f"Error: no se puede crear el usuario")
                return None
            
            user_id = user_result.data[0]["id"]

            #Crear perfil en tabla profiles
            profile_data = {
            "id": user_id,
            "full_name": user_data.full_name,
            "stage": user_data.stage,
            # Guardar business_type en objectives como JSON
            "objectives": {
                "business_type": user_data.business_type
            }
        }

            profile_result = self.db.table('profiles').insert(profile_data).execute()
            print(f"Perfil creado {profile_result.data}")

            try:
                asyncio.create_task(email_service.send_verification_email(user_data.email, user_data.full_name))
            except Exception as e:
                print(f"Error enviando email de verificacion: {e}")

            if profile_result.data:
                profile = profile_result.data[0]
                return UserResponse(
                    id=str(user_id),
                    email=user_data.email,
                    full_name=profile["full_name"],
                    business_type=profile.get("objectives", {}).get("business_type", "producto"),
                    stage=profile["stage"],
                    created_at=profile['created_at'],
                    is_verified = False
            )
            return None
    
        except Exception as e:
                print(f"❌ Error creando usuario: {e}")
                import traceback
                print(f"📊 Traceback: {traceback.format_exc()}")
                return None


    
    def authenticate_user(self, login_data:UserLogin) -> Optional[UserResponse]:
        """Autenticar usuario"""
        try:
            print(f"Autenticando usuario: {login_data.email}")

            #Obtain user
            user_result = self.db.table('users').select('*').eq('email',login_data.email).execute()
            print(f"Resultado no encontrado: {len(user_result.data) if user_result.data else 0} registros encontrados")

            if not user_result.data: 
                print(f"Usuario no encontrado: {login_data.email}")
                return None
            
            user = user_result.data[0]

            #Verify password
            password_valid = verify_password(login_data.password,user["password_hash"])
            print(f"🔐 Verificación de contraseña: {'✅ Válida' if password_valid else '❌ Inválida'}")
            if not password_valid:
                print("Contrasena incorrecta")
                return None
            
            #Verify if user is verified
            if not user.get("is_verified",False):
                print("Usuario no verificado")
                return None

            #Obtain profile
            profile_result = self.db.table('profiles').select('*').eq('id',user["id"]).execute()
            print(f"📋 Resultado búsqueda perfil: {len(profile_result.data) if profile_result.data else 0} registros encontrados")

            if not profile_result.data:
                print("Perfil no encontrado")
                return None
            
            profile = profile_result.data[0]
            print(f"✅ Usuario autenticado exitosamente: {user['email']}")

            return UserResponse(
            id=str(user["id"]),
            email=user["email"],
            full_name=profile["full_name"],
            business_type=profile.get("objectives", {}).get("business_type", "producto"),  
            stage=profile["stage"],
            created_at=profile['created_at'],
            is_verified= user.get("is_verified",False)
        )
        
        except Exception as e:
            print(f"Error autenticando usuario: {e}")
            return None


    
    def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        """Obtener usuario por email"""
        try:
            #Obtain user
            user_result = self.db.table('users').select('*').eq('email', email).execute()

            if not user_result.data:
                return None
            
            user = user_result.data[0]

            #Obtain profile
            profile_result = self.db.table('profiles').select('*').eq('id',user["id"]).execute()

            if not profile_result.data:
                return None
            
            profile = profile_result.data[0]

            return UserResponse(
            id=str(user["id"]),
            email=user["email"],
            full_name=profile["full_name"],
            business_type=profile.get("objectives", {}).get("business_type", "producto"), 
            stage=profile["stage"],
            created_at=profile["created_at"],
            is_verified=user.get("is_verified",False)
        )
        except Exception as e:
            print(f"Error getting user by email: {e}")
            return None
    def set_user_verified(self,email:str)->bool:
        """"Marcar usuario como verificado"""
        try:
            result = self.db.table('users').update({"is_verified":True}).eq('email',email).execute()
            print(f"Usuario marcado como verificado: {email}")
            return bool(result.data)
        except Exception as e:
            print(f"Error marcando usuario como verificado: {e}")
            return False
        
    async def resend_verification_email(self,email:str,full_name:str):
        await email_service.send_verification_email(email,full_name)


# Instancia global del servicio
user_service = UserService()