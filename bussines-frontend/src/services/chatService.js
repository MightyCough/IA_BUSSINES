import { chatAPI } from "./api.js";

class ChatService{

    /**
     * Enviar mensaje a la IA y recibir respuesta 
     * @param {string} message - mensaje del usuario
     * @param {Array} conversationHistory - historial de conversacion (opcional)
     * @returns {Promise<objects>} - Respusta de la IA
     */

    async sendMessage(message,conversationHistory = []){
        try{
            const response = await chatAPI.sendMessage({
                message:message,
                conversation_history:conversationHistory
            })
            return {
                success: true,
                data: response.data
            }
        }catch(error){
            console.error('Error enviando mensaje:', error)
            console.error('Error details:', {
                message: error.message,
                status: error.response?.status,
                data: error.response?.data,
                config: error.config
            })

            return {
                success:false,
                error: error.response?.data?.detail || 'Error conectando con la IA'
            }
        }
    }
    /**
   * 🔥 NUEVOS MÉTODOS PARA HISTORIAL
   */
  
  // Conversaciones
  async getConversations() {
    try {
      const response = await chatAPI.getConversations()
      return {
        success: true,
        data: response.data
      }
    } catch (error) {
      console.error('Error obteniendo conversaciones:', error)
      return {
        success: false,
        error: error.response?.data?.detail || 'Error obteniendo conversaciones'
      }
    }
  }

  async createConversation(title = 'Nueva conversación') {
    try {
      const response = await chatAPI.createConversation({ title })
      return {
        success: true,
        data: response.data
      }
    } catch (error) {
      console.error('Error creando conversación:', error)
      return {
        success: false,
        error: error.response?.data?.detail || 'Error creando conversación'
      }
    }
  }

  async deleteConversation(conversationId) {
    try {
      const response = await chatAPI.deleteConversation(conversationId)
      return {
        success: true,
        data: response.data
      }
    } catch (error) {
      console.error('Error eliminando conversación:', error)
      return {
        success: false,
        error: error.response?.data?.detail || 'Error eliminando conversación'
      }
    }
  }

  // Mensajes
  async getMessages(conversationId) {
    try {
      const response = await chatAPI.getMessages(conversationId)
      return {
        success: true,
        data: response.data
      }
    } catch (error) {
      console.error('Error obteniendo mensajes:', error)
      return {
        success: false,
        error: error.response?.data?.detail || 'Error obteniendo mensajes'
      }
    }
  }

  async sendMessageToConversation(conversationId, content) {
    try {
      const response = await chatAPI.sendMessageToConversation(conversationId, { content })
      return {
        success: true,
        data: response.data
      }
    } catch (error) {
      console.error('Error enviando mensaje a conversación:', error)
      return {
        success: false,
        error: error.response?.data?.detail || 'Error enviando mensaje'
      }
    }
  }



    /**
     * Probar conexion con la IA
     * @return {Promise<objects>} - Resultado de test
     */
    async testConnection(){
        try{
            const response = await chatAPI.testChat()

            return {
                success:true,
                data:response.data
            }
        }catch(error){
            console.error('❌ Error en test de IA:', error)
            console.error('❌ Error details:', {
                message: error.message,
                code: error.code,
                status: error.response?.status,
                statusText: error.response?.statusText,
                data: error.response?.data,
                url: error.config?.url,
                method: error.config?.method
            })

            return{
                success: false,
                error: error.message
            }
        }
    }
}

export const chatService = new ChatService()
export default chatService