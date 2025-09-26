from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Optional
from app.services.ai_service import ai_service

router = APIRouter()

class ChatMessage(BaseModel):
    message: str
    conversation_history: Optional[List[Dict]] = []

class ChatResponse(BaseModel):
    response: str
    status: str = "success"
    source: str = "ai"  # "ai" o "simulator"

@router.post("/message", response_model=ChatResponse)
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
        
        return ChatResponse(
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