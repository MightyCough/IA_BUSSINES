import httpx
import json
import random
from typing import List, Dict
from app.core.config import settings

class AIService:
    def __init__(self):
        # ✅ CONFIGURAR OPENROUTER
        self.openrouter_api_key = settings.OPENROUTER_API_KEY
        self.openrouter_url = "https://openrouter.ai/api/v1/chat/completions"

        #Debug Info
        print("Inicializando AIService...")
        print(f"API Key configurada: {bool(self.openrouter_api_key)}")
        if self.openrouter_api_key:
            print(f"API Key length: {len(self.openrouter_api_key)}")
            print(f"API Key preview: {self.openrouter_api_key[:15]}...{self.openrouter_api_key[-5]}")


        
    async def generate_business_response(
        self, 
        user_message: str, 
        user_context: Dict = None,
        conversation_history: List[Dict] = None
    ) -> str:
        """
        Genera respuesta usando OpenRouter o simulador
        """
        try:
            # ✅ SI HAY API KEY, USAR OPENROUTER REAL
            if self.openrouter_api_key and self.openrouter_api_key != "":
                print(f"Usando OpenRouter con API key: {self.openrouter_api_key[:20]}...")
                return await self._openrouter_response(user_message, user_context, conversation_history)
            else:
                print("Usando simulador inteligente")
                return await self._simulate_response(user_message, user_context)
                
        except Exception as e:
            print(f"Error en AI Service: {e}")
            return await self._simulate_response(user_message, user_context)
    
    async def _openrouter_response(self, user_message: str, user_context: Dict, conversation_history: List[Dict]) -> str:
        """
        Llamada real a OpenRouter API
        """
        try:
            print(f"🔑 API Key presente: {bool(self.openrouter_api_key)}")
            print(f"🔑 API Key length: {len(self.openrouter_api_key) if self.openrouter_api_key else 0}")
            print(f"🔑 API Key starts with: {self.openrouter_api_key[:10]}...")
            system_prompt = self._build_system_prompt(user_context)
            
            messages = [{"role": "system", "content": system_prompt}]   
            
            if conversation_history:
                messages.extend(conversation_history[-6:])
            
            messages.append({"role": "user", "content": user_message})
            
            payload = {
                "model": "mistralai/mistral-7b-instruct:free",  # ✅ MODELO GRATIS
                "messages": messages,
                "max_tokens": 1000,
                "temperature": 0.7,
                "stream": False
            }
            
            headers = {
                "Authorization": f"Bearer {self.openrouter_api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": settings.FRONTEND_URL,
                "X-Title": "AI Business Advisor"
            }

            print(f"🚀 Enviando request a: {self.openrouter_url}")
            print(f"🎯 Modelo: {payload['model']}")
            print(f"📝 Mensaje: {user_message[:50]}...")
            
            print(f"🚀 Enviando request a OpenRouter...")
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.openrouter_url,
                    headers=headers,
                    json=payload,
                    timeout=45.0
                )
                
                print(f"📡 Status Code: {response.status_code}")
                print(f"📡 Response Headers: {dict(response.headers)}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"📊 Response data keys: {list(data.keys())}")

                    # ✅ DEBUG: VER CONTENIDO DE LA RESPUESTA
                    print(f"🔍 Full response: {json.dumps(data, indent=2)}")
                    
                    ai_response = data["choices"][0]["message"]["content"]
                    print(f"✅ Mistral SUCCESS: {len(ai_response)} chars")
                    return ai_response
                else:
                    print(f"❌ Error OpenRouter: {response.status_code}")
                    print(f"❌ Error body: {response.text}")
                    return await self._simulate_response(user_message, user_context)
                    
        except httpx.TimeoutException as e:
            print(f"⏰ Timeout error: {e}")
            return await self._simulate_response(user_message, user_context)
        except httpx.RequestError as e:
            print(f"🌐 Request error: {e}")
            return await self._simulate_response(user_message, user_context)
        except Exception as e:
            print(f"❌ Exception en OpenRouter: {type(e).__name__}: {e}")
            return await self._simulate_response(user_message, user_context)

    async def _simulate_response(self, user_message: str, user_context: Dict) -> str:
        """
        Simulador inteligente como fallback
        """
        message_lower = user_message.lower()
        
        if any(word in message_lower for word in ['hola', 'hello', 'buenas', 'saludos']):
            responses = [
                """¡Hola! 👋 Soy tu asesor empresarial de IA.

🎯 **¿En qué puedo ayudarte hoy?**
- Validación de ideas de negocio
- Estrategias de marketing y ventas  
- Planificación financiera
- Análisis de mercado

💡 Cuéntame sobre tu proyecto para darte consejos específicos."""
            ]
        else:
            responses = [
                f"""📋 **ANÁLISIS DE TU CONSULTA:**

"{user_message[:100]}{'...' if len(user_message) > 100 else ''}"

**🎯 Mi recomendación:**

1. **Análisis de situación**: Evalúa recursos y limitaciones actuales
2. **Objetivos claros**: Define metas específicas y medibles  
3. **Plan de acción**: Divide en pasos manejables
4. **Ejecución**: Implementa consistentemente

💡 **Tip**: El éxito = Estrategia correcta × Ejecución consistente"""
            ]
        
        response = random.choice(responses)
        
        if user_context:
            name = user_context.get('full_name', 'Emprendedor')
            response = f"¡Hola **{name}**! 👋\n\n" + response
        
        response += f"\n\n🎭 **Modo**: Simulador (OpenRouter configurado pero falló)"
        
        return response
    
    def _build_system_prompt(self, user_context: Dict = None) -> str:
        """
        Prompt mejorado para conversaciones continuas
        """
        base_prompt = """Eres un asesor empresarial experto con 15+ años de experiencia.

IMPORTANTE: Mantén el contexto de la conversación. Si ya te han presentado o ya han hablado antes, NO repitas saludos ni presentaciones.

Tu misión: Dar consejos prácticos y estratégicos para emprendedores.

Reglas de conversación:
- PRIMER MENSAJE: Saluda calurosamente y preséntate
- MENSAJES SIGUIENTES: Continúa la conversación naturalmente, SIN repetir saludos
- Si alguien pregunta algo nuevo, ayúdales directamente
- Mantén un tono profesional pero cercano
- Siempre en español

Estilo de respuesta:
- Estructurado y organizado
- Incluye pasos actionables concretos
- Máximo 400 palabras por respuesta
- Usa emojis ocasionalmente para dar calidez

Formato recomendado:
1. Respuesta directa a la consulta
2. Recomendaciones específicas (2-3 puntos)
3. Pregunta de seguimiento o próximo paso"""
    
        if user_context:
            user_info = f"""

Información del usuario:
- Nombre: {user_context.get('full_name', 'Emprendedor')}
- Tipo de negocio: {user_context.get('business_type', 'General')} 
- Etapa: {user_context.get('stage', 'Idea')}

Personaliza tus respuestas considerando esta información."""
            base_prompt += user_info
        
        return base_prompt

# ✅ INSTANCIA GLOBAL
ai_service = AIService()