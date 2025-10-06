import { defineStore } from 'pinia'
import { chatService } from '../services/chatService'

export const useChatStore = defineStore('chat', {
  state: () => ({
    // Modo simple (chat directo)
    simpleMessages: [],
    isSimpleMode: true,
    
    // Modo historial (conversaciones)
    conversations: [],
    currentConversation: null,
    messages: [],
    
    // Estado general
    isLoading: false,
    error: null
  }),

  getters: {
    getCurrentMessages: (state) => {
      return state.isSimpleMode ? state.simpleMessages : state.messages
    },
    
    hasConversations: (state) => state.conversations.length > 0,
    
    isHistoryMode: (state) => !state.isSimpleMode
  },

  actions: {
    // 🔥 MODO SIMPLE
    async sendSimpleMessage(content) {
      try {
        // Agregar mensaje del usuario inmediatamente
        const userMessage = {
          id: Date.now(),
          role: 'user',
          content,
          created_at: new Date().toISOString()
        }
        this.simpleMessages.push(userMessage)
        this.isLoading = true

        // Enviar al backend
        const result = await chatService.sendMessage(content, this.simpleMessages)
        
        if (result.success) {
          // Agregar respuesta de IA
          const aiMessage = {
            id: Date.now() + 1,
            role: 'assistant',
            content: result.data.response,
            created_at: new Date().toISOString()
          }
          this.simpleMessages.push(aiMessage)
        } else {
          throw new Error(result.error)
        }

      } catch (error) {
        this.error = error.message
        // Agregar mensaje de error
        this.simpleMessages.push({
          id: Date.now() + 1,
          role: 'assistant',
          content: 'Lo siento, hubo un error al procesar tu mensaje. Intenta de nuevo.',
          created_at: new Date().toISOString()
        })
        throw error
      } finally {
        this.isLoading = false
      }
    },

    clearSimpleChat() {
      this.simpleMessages = []
    },

    // 🔥 MODO HISTORIAL
    async loadConversations() {
      try {
        this.isLoading = true
        const result = await chatService.getConversations()
        
        if (result.success) {
          this.conversations = result.data
        } else {
          throw new Error(result.error)
        }
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async createConversation(title) {
      try {
        const result = await chatService.createConversation(title)
        
        if (result.success) {
          const conversation = result.data
          this.conversations.unshift(conversation)
          this.currentConversation = conversation
          this.messages = []
          this.isSimpleMode = false
          return conversation
        } else {
          throw new Error(result.error)
        }
      } catch (error) {
        this.error = error.message
        throw error
      }
    },

    async selectConversation(conversation) {
      try {
        this.currentConversation = conversation
        this.isLoading = true
        
        const result = await chatService.getMessages(conversation.id)
        
        if (result.success) {
          this.messages = result.data
          this.isSimpleMode = false
        } else {
          throw new Error(result.error)
        }
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async sendMessage(content) {    
      if (!this.currentConversation) {
        await this.createConversation('Nueva conversación')
      }

      try {
        // Agregar mensaje del usuario inmediatamente
        const userMessage = {
          id: `temp-${Date.now()}`,
          conversation_id: this.currentConversation.id,
          role: 'user',
          content,
          created_at: new Date().toISOString()
        }
        this.messages.push(userMessage)

        // Enviar al backend
        const result = await chatService.sendMessageToConversation(
          this.currentConversation.id, 
          content
        )
        
        if (result.success) {
          // Reemplazar mensaje temporal con los reales del backend
          const response = result.data
          
          // Actualizar mensaje del usuario con el ID real
          const userIndex = this.messages.findIndex(m => m.id === userMessage.id)
          if (userIndex !== -1) {
            this.messages[userIndex] = response.user_message
          }
          
          // Agregar respuesta de IA
          this.messages.push(response.assistant_message)
          
          // Actualizar lista de conversaciones
          await this.loadConversations()
        } else {
          throw new Error(result.error)
        }

      } catch (error) {
        this.error = error.message
        // Agregar mensaje de error
        this.messages.push({
          id: Date.now() + 1,
          role: 'assistant',
          content: 'Error al enviar mensaje. Intenta de nuevo.',
          created_at: new Date().toISOString()
        })
        throw error
      }
    },

    async deleteConversation(conversationId) {
      try {
        const result = await chatService.deleteConversation(conversationId)
        
        if (result.success) {
          this.conversations = this.conversations.filter(c => c.id !== conversationId)
          
          if (this.currentConversation?.id === conversationId) {
            this.currentConversation = null
            this.messages = []
            this.isSimpleMode = true
          }
        } else {
          throw new Error(result.error)
        }
      } catch (error) {
        this.error = error.message
        throw error
      }
    },

    // 🔥 UTILIDADES
    toggleMode() {
      this.isSimpleMode = !this.isSimpleMode
    },

    async loadConversationsIfNeeded() {
      if (!this.isSimpleMode && this.conversations.length === 0) {
        await this.loadConversations()
      }
    },

    enableHistoryMode() {
      this.isSimpleMode = false
      this.loadConversations()
    },

    clearError() {
      this.error = null
    }
  }
})