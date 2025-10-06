from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from app.core.database import supabase
from app.schemas.chat import Conversation, Message, ConversationCreate, MessageCreate
from app.services.ai_service import ai_service

class ChatService:
    
    async def create_conversation(self, user_id: str, title: str = "Nueva conversación") -> dict:
        """Crear nueva conversación"""
        try:
            result = supabase.table("conversations").insert({
                "user_id": user_id,
                "title": title,
                "is_archived": False
            }).execute()
            
            if result.data and len(result.data) > 0:
                return result.data[0]
            else:
                raise Exception("No se pudo crear la conversación")
        except Exception as e:
            raise Exception(f"Error al crear conversación: {str(e)}")

    async def get_user_conversations(self, user_id: str, include_archived: bool = False) -> List[dict]:
        """Obtener conversaciones del usuario"""
        try:
            query = supabase.table("conversations").select("*").eq("user_id", user_id)
            
            if not include_archived:
                query = query.eq("is_archived", False)
                
            result = query.order("updated_at", desc=True).execute()
            return result.data or []
        except Exception as e:
            raise Exception(f"Error al obtener conversaciones: {str(e)}")

    async def get_conversation_messages(self, conversation_id: str, user_id: str) -> List[dict]:
        """Obtener mensajes de una conversación (verificando que pertenezca al usuario)"""
        try:
            # Verificar que la conversación pertenece al usuario
            conv_result = supabase.table("conversations") \
                .select("id") \
                .eq("id", conversation_id) \
                .eq("user_id", user_id) \
                .execute()
            
            if not conv_result.data:
                raise Exception("Conversación no encontrada o sin acceso")
            
            # Obtener mensajes
            result = supabase.table("messages") \
                .select("*") \
                .eq("conversation_id", conversation_id) \
                .order("created_at", desc=False) \
                .execute()
            
            return result.data or []
        except Exception as e:
            raise Exception(f"Error al obtener mensajes: {str(e)}")

    async def send_message(self, user_id: str, conversation_id: str, content: str) -> dict:
        """Enviar mensaje y obtener respuesta de IA"""
        try:
            # Verificar que la conversación pertenece al usuario
            conv_result = supabase.table("conversations") \
                .select("id") \
                .eq("id", conversation_id) \
                .eq("user_id", user_id) \
                .execute()
            
            if not conv_result.data:
                raise Exception("Conversación no encontrada o sin acceso")

            # 1. Guardar mensaje del usuario
            user_message_result = supabase.table("messages").insert({
                "conversation_id": conversation_id,
                "role": "user",
                "content": content,
                "metadata": {}
            }).execute()
            
            if not user_message_result.data:
                raise Exception("Error al guardar mensaje del usuario")

            # 2. Obtener historial para contexto (últimos 10 mensajes)
            messages_history = await self.get_conversation_messages(conversation_id, user_id)
            
            # Preparar contexto para la IA (solo los últimos mensajes para no sobrecargar)
            context_messages = messages_history[-20:] if len(messages_history) > 20 else messages_history
            
            # 3. Generar respuesta de IA
            ai_response = await ai_service.generate_response(content, context_messages)
            
            # 4. Guardar respuesta de IA
            assistant_message_result = supabase.table("messages").insert({
                "conversation_id": conversation_id,
                "role": "assistant", 
                "content": ai_response,
                "metadata": {}
            }).execute()
            
            if not assistant_message_result.data:
                raise Exception("Error al guardar respuesta de IA")

            # 5. Actualizar timestamp de conversación
            supabase.table("conversations") \
                .update({"updated_at": datetime.now().isoformat()}) \
                .eq("id", conversation_id) \
                .execute()

            return {
                "conversation_id": conversation_id,
                "user_message": user_message_result.data[0],
                "assistant_message": assistant_message_result.data[0]
            }
            
        except Exception as e:
            raise Exception(f"Error al enviar mensaje: {str(e)}")

    async def delete_conversation(self, conversation_id: str, user_id: str) -> bool:
        """Eliminar conversación y todos sus mensajes"""
        try:
            result = supabase.table("conversations") \
                .delete() \
                .eq("id", conversation_id) \
                .eq("user_id", user_id) \
                .execute()
            
            return len(result.data) > 0 if result.data else False
        except Exception as e:
            raise Exception(f"Error al eliminar conversación: {str(e)}")

    async def archive_conversation(self, conversation_id: str, user_id: str) -> bool:
        """Archivar conversación (soft delete)"""
        try:
            result = supabase.table("conversations") \
                .update({"is_archived": True}) \
                .eq("id", conversation_id) \
                .eq("user_id", user_id) \
                .execute()
            
            return len(result.data) > 0 if result.data else False
        except Exception as e:
            raise Exception(f"Error al archivar conversación: {str(e)}")

    async def update_conversation_title(self, conversation_id: str, user_id: str, title: str) -> bool:
        """Actualizar título de conversación"""
        try:
            result = supabase.table("conversations") \
                .update({"title": title, "updated_at": datetime.now().isoformat()}) \
                .eq("id", conversation_id) \
                .eq("user_id", user_id) \
                .execute()
            
            return len(result.data) > 0 if result.data else False
        except Exception as e:
            raise Exception(f"Error al actualizar título: {str(e)}")

    async def get_conversation_with_messages(self, conversation_id: str, user_id: str) -> dict:
        """Obtener conversación completa con sus mensajes"""
        try:
            # Obtener conversación
            conv_result = supabase.table("conversations") \
                .select("*") \
                .eq("id", conversation_id) \
                .eq("user_id", user_id) \
                .execute()
            
            if not conv_result.data:
                raise Exception("Conversación no encontrada")
            
            conversation = conv_result.data[0]
            
            # Obtener mensajes
            messages = await self.get_conversation_messages(conversation_id, user_id)
            
            conversation["messages"] = messages
            return conversation
            
        except Exception as e:
            raise Exception(f"Error al obtener conversación: {str(e)}")

# Instancia global
chat_service = ChatService()


