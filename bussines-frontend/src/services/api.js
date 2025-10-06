import axios from 'axios'

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1'

console.log('API Base URL: ', API_BASE_URL)

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 60000 // 60 segundos timeout
})

// ✅ INTERCEPTOR DE REQUEST - AGREGAR TOKEN AUTOMÁTICAMENTE
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
      console.log('🔑 Token enviado:', token.substring(0, 30) + '...')
      console.log('🎯 URL:', config.url)
      console.log('📤 Método:', config.method.toUpperCase())
    } else {
      console.warn('⚠️ No se encontró token en localStorage')
    }
    return config
  },
  (error) => {
    console.error('❌ Request interceptor error:', error)
    return Promise.reject(error)
  }
)

// Interceptor para añadir token automáticamente
api.interceptors.response.use(
  (response) => {
    console.log(`✅ ${response.config.method?.toUpperCase()} ${response.config.url} - ${response.status}`)
    return response
  },
  (error) => {
    console.error('❌ API Error:', error.message)
    console.error('❌ API Error details:', {
      message: error.message,
      status: error.response?.status,
      data: error.response?.data,
      url: error.config?.url
    })
    
    // ✅ MEJORAR MANEJO DEL 401
    if (error.response?.status === 401) {
      console.error('🚨 Error 401: Token inválido o expirado')
      
      // Limpiar storage
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      
      // Solo redirigir si no estamos ya en login
      if (!window.location.pathname.includes('/login')) {
        console.log('🔄 Redirigiendo a login...')
        window.location.href = '/login'
      }
    }
    
    return Promise.reject(error)
  }
)


// Interceptor para manejar errores
api.interceptors.response.use(
  (response) => {
    console.log('✅ Response:', response.status, response.config.url);
    return response
  },
  (error) => {
    console.error('❌ API Error:', error)
    console.error('❌ API Error details:', {
      message: error.message,
      status: error.response?.status,
      data: error.response?.data,
      url: error.config?.url
    })
    
    if (error.response?.status === 401) {
      // Token expirado o inválido
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      
      // Solo redirigir si no estamos ya en login/register
      if (!window.location.pathname.includes('/login') && 
          !window.location.pathname.includes('/register')) {
        window.location.href = '/login'
      }
    }
    
    return Promise.reject(error)
  }
)

// ✅ AGREGAR MÉTODOS PARA CHAT
export const chatAPI = {
  // Chat directo (sin historial)
  async sendMessage(data) {
    return await api.post('/chat/message', data)
  },
  
  async testChat() {
    return await api.get('/chat/test')
  },
  
  // Conversaciones (para historial)
  async getConversations() {
    return await api.get('/chat/conversations')
  },
  
  async createConversation(data) {
    return await api.post('/chat/conversations', data)
  },
  
  async deleteConversation(conversationId) {
    return await api.delete(`/chat/conversations/${conversationId}`)
  },
  
  // Mensajes
  async getMessages(conversationId) {
    return await api.get(`/chat/conversations/${conversationId}/messages`)
  },
  
  async sendMessageToConversation(conversationId, data) {
    return await api.post(`/chat/conversations/${conversationId}/messages`, data)
  }
}


export const authAPI = {
  requestRegister:(UserData)=>api.post('auth/request-register',UserData),
  verifyRegister:(data) => api.post('auth/register/verify',data),
  login:(credentials) => api.post('/auth/login',credentials),
  me: () => api.get('/auth/me'),
}
export default api