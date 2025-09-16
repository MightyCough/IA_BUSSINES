from typing import Optional, Dict, List
from datetime import datetime
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.core.security import get_password_hash, verify_password

class UserService:
    """Servicio para manejar usuarios en memoria"""
    
    def __init__(self):
        # "Base de datos" en memoria
        self._users: Dict[str, dict] = {}
        self._user_counter = 1
        
        # Usuario de prueba
        self.create_user(UserCreate(
            name="Usuario Test",
            email="test@example.com",
            password="123456"
        ))
    
    def create_user(self, user_data: UserCreate) -> Optional[UserResponse]:
        """Crear nuevo usuario"""
        # Verificar si ya existe
        if user_data.email in self._users:
            return None
        
        # Crear usuario
        user_id = f"user_{self._user_counter}"
        self._user_counter += 1
        
        new_user = {
            "id": user_id,
            "name": user_data.name,
            "email": user_data.email,
            "hashed_password": get_password_hash(user_data.password),
            "created_at": datetime.utcnow().isoformat()
        }
        
        self._users[user_data.email] = new_user
        
        return UserResponse(
            id=new_user["id"],
            name=new_user["name"],
            email=new_user["email"],
            created_at=new_user["created_at"]
        )
    
    def authenticate_user(self, email: str, password: str) -> Optional[UserResponse]:
        """Autenticar usuario"""
        user = self._users.get(email)
        if not user:
            return None
        
        if not verify_password(password, user["hashed_password"]):
            return None
        
        return UserResponse(
            id=user["id"],
            name=user["name"],
            email=user["email"],
            created_at=user["created_at"]
        )
    
    def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        """Obtener usuario por email"""
        user = self._users.get(email)
        if not user:
            return None
        
        return UserResponse(
            id=user["id"],
            name=user["name"],
            email=user["email"],
            created_at=user["created_at"]
        )
    
    def get_user_by_id(self, user_id: str) -> Optional[UserResponse]:
        """Obtener usuario por ID"""
        for user in self._users.values():
            if user["id"] == user_id:
                return UserResponse(
                    id=user["id"],
                    name=user["name"],
                    email=user["email"],
                    created_at=user["created_at"]
                )
        return None
    
    def update_user(self, user_id: str, user_update: UserUpdate) -> Optional[UserResponse]:
        """Actualizar usuario"""
        # Buscar usuario
        user = None
        old_email = None
        for email, user_data in self._users.items():
            if user_data["id"] == user_id:
                user = user_data
                old_email = email
                break
        
        if not user:
            return None
        
        # Actualizar campos
        if user_update.name is not None:
            user["name"] = user_update.name
        
        return UserResponse(
            id=user["id"],
            name=user["name"],
            email=user["email"],
            created_at=user["created_at"]
        )
    
    def get_all_users(self) -> List[UserResponse]:
        """Obtener todos los usuarios (para testing)"""
        return [
            UserResponse(
                id=user["id"],
                name=user["name"],
                email=user["email"],
                created_at=user["created_at"]
            )
            for user in self._users.values()
        ]

    def delete_user(self, user_id:str) -> bool:
        """"Eliminar usuario por ID"""
        for email, user in list(self._users.items()):
            if user["id"] == user_id:
                del self._users[email]
                return True
        return False

# Instancia global del servicio
user_service = UserService()