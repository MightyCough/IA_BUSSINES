from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Optional
from app.schemas.chat import ConversationCreate,Message,Conversation,MessageCreate,ChatResponse
from app.services.ai_service import ai_service
from app.services.chat_service import chat_service
from app.core.security import get_current_user

router = APIRouter()

class ChatMessage(BaseModel):
    message: str
    conversation_history: Optional[List[Dict]] = []

class ChatResponseSimple(BaseModel):
    response: str
    status: str = "success"
    source: str = "ai"  # "ai" o "simulator"

@router.post("/message", response_model=ChatResponseSimple)
async def chat_with_ai(chat_data: ChatMessage):
    """
    Endpoint principal para chat con IA
    """
    try:
        print(f"📩 Mensaje recibido: {chat_data.message[:50]}...")
        
        # Contexto simulado (después lo sacaremos del JWT)
        user_context = {
            "full_name": "Emprendedor Demo",
            "business_type": "producto",
            "stage": "idea",
            "email": "demo@test.com"
        }
        
        # ✅ GENERAR RESPUESTA
        ai_response = await ai_service.generate_business_response(
            user_message=chat_data.message,
            user_context=user_context,
            conversation_history=chat_data.conversation_history
        )
        
        # Detectar si es simulador o IA real
        source = "simulator" if "simulador" in ai_response.lower() else "ai"
        
        return ChatResponseSimple(
            response=ai_response,
            status="success",
            source=source
        )
        
    except Exception as e:
        print(f"❌ Error en chat endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error procesando el mensaje"
        )

@router.get("/test")
async def test_ai():
    """
    Endpoint de prueba
    """
    try:
        print("🧪 Ejecutando test de IA...")
        
        test_response = await ai_service.generate_business_response(
            user_message="Hola, quiero validar mi idea de negocio de productos orgánicos",
            user_context={
                "full_name": "Usuario Test",
                "business_type": "producto",
                "stage": "idea"
            }
        )
        
        return {
            "status": "success",
            "test_message": "Hola, quiero validar mi idea de negocio de productos orgánicos",
            "ai_response": test_response,
            "openrouter_configured": bool(ai_service.openrouter_api_key)
        }
        
    except Exception as e:
        print(f"❌ Error en test: {e}")
        return {
            "status": "error", 
            "error": str(e),
            "openrouter_configured": bool(ai_service.openrouter_api_key)
        }
    

@router.post("/conversations",response_model=dict)
async def create_conversation(
    conversation_data: ConversationCreate,
    current_user:dict = Depends(get_current_user)
):
    """Crear nueva conversacion"""
    try:
        return await chat_service.create_conversation(
            user_id=current_user["id"],
            title=conversation_data.title or "Nueva conversacion"
        )
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))

@router.get("/conversations",response_model=List[dict])
async def get_conversations(
    include_archived:bool = False,
    current_user:dict = Depends(get_current_user)
):
    """Obtener conversacion del usuario"""
    try:
        return await chat_service.get_user_conversations(
            user_id=current_user["id"],
            include_archived=include_archived
        )
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))
    
@router.get("/conversations/{conversation_id}",response_model=dict)
async def get_conversation_detail(
    conversation_id:str,
    current_user:dict = Depends(get_current_user)
):
    """Obtener conversacion con mensajes"""
    try:
        return await chat_service.get_conversation_messages(
            conversation_id=conversation_id,
            user_id=current_user["id"]
        )
    except Exception as e:
        raise HTTPException(status_code=404,detail=str(e))
    
@router.get("/conversations/{conversation_id}/messages",response_model=List[dict])
async def get_conversation_messages(
    conversation_id:str,
    current_user:dict = Depends(get_current_user)
):
    """Obtener mensajes de una conversacion"""
    try:
        return await chat_service.get_conversation_messages(
            conversation_id=conversation_id,
            user_id=current_user["id"]
        )
    except Exception as e:
        raise HTTPException(status_code=404,detail=str(e))
    
@router.post("/conversations/{conversation_id}/messages",response_model=dict)
async def send_message(
    conversation_id:str,
    message_data:MessageCreate,
    current_user:dict = Depends(get_current_user)
):
    """Enviar mensaje de conversacion"""
    try:
        return await chat_service.send_message(
            user_id=current_user["id"],
            conversation_id=conversation_id,
            content=message_data.content
        )
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))
    
@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id:str,
    current_user:dict = Depends(get_current_user)
):
    """Eliminar conversacion permanentemente"""
    try:
        success = await chat_service.delete_conversation(conversation_id,current_user["id"])
        if not success:
            raise HTTPException(status_code-404,detail="Conversacion no encontrada")
        return {"message":"Conversacion eliminada"}
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))
    
@router.patch("/conversations/{conversation_id}/archive")
async def archive_conversation(
    conversation_id:str,
    current_user:dict = Depends(get_current_user)
):
    """Archivar conversacion"""
    try:
        succcess = await chat_service.archive_conversation(conversation_id,current_user["id"])
        if not succcess:
            raise HTTPException(status_code=404,detail="Conversacion no encontrada")
        return {"message":"Conversacion archivada"}
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))
    
@router.put("/conversations/{conversation_id}/title")
async def update_conversation_title(
    conversation_id:str,
    title:str,
    current_user:dict = Depends(get_current_user)
):
    """Actualizar titulo de conversacion"""
    try:
        success = await chat_service.update_conversation_title(
            conversation_id,current_user["id"],title
        )
        if not success:
            raise HTTPException(status_code=404,detail="Conversacion no encontrada")
        return {"message":"Titulo actualizado"}
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))