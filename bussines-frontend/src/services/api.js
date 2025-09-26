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

// Interceptor para añadir token automáticamente
api.interceptors.request.use(
  (config) => {
    console.log('📡 Request:', config.method?.toUpperCase(), config.url); 
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    console.error('❌ Request error:', error);
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


export const authAPI = {
  register: (userData) => api.post('/auth/register',userData),
  login:(credentials) => api.post('/auth/login',credentials),
  me: () => api.get('/auth/me'),
}

export const chatAPI = {
  sendMessage: (messageData) => api.post('/chat/message',messageData),
  testChat: () =>api.get('/chat/test'),
}

export default api