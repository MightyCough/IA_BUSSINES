import { authAPI } from './api.js'

export const authService = {
  // Registro (Paso 1: solo manda código al correo)
  async register(userData) {
    try {
      const response = await authAPI.register({
        email: userData.email,
        password: userData.password,
        full_name: userData.full_name,
        business_type: userData.business_type || 'producto',
        stage: userData.stage || 'idea'
      })

      // 👉 Guardamos el email temporalmente
      if (response.data.email) {
        localStorage.setItem('pending_email', response.data.email)
      }

      return response.data
    } catch (error) {
      console.error('Register error:', error)
      throw error.response?.data || error
    }
  },

  async requestRegister(userData) {
    try {
      const response = await authAPI.requestRegister(userData)
      
      if (response.status === 200 || response.status === 201) {
        return {
          success: true,
          data: response.data
        }
      } else {
        return {
          success: false,
          error: 'Error en el registro'
        }
      }
    } catch (error) {
      console.error('Error en registro:', error)
      return {
        success: false,
        error: error.response?.data?.detail || error.message || 'Error de conexión'
      }
    }
  },


  // Verificar email (Paso 2: validar código y crear usuario en BD)
  async verifyEmail(verificationCode) {
    try {
      const email = (localStorage.getItem('pending_email') || "").trim().toLowerCase()
      if (!email) {
        throw new Error('No se encontró email pendiente en localStorage')
      }

      const response = await authAPI.verifyRegister({
        email,
        verification_code: String(verificationCode)
      })

      const data = response.data
       // ⬇️ GUARDA TOKEN Y USER
    if (data?.access_token) {
      localStorage.setItem('token', data.access_token)
      localStorage.setItem('user', JSON.stringify(data.user))
    }

      // ✅ Si todo bien, borramos pending_email
      localStorage.removeItem('pending_email')

      return data
    } catch (error) {
      console.error('Verification error:', error)
      throw error.response?.data || error
    }
  },

  // Login
  async login(credentials) {
    try {
      console.log('🔄 Intentando login con:', credentials.email)
      
      const response = await authAPI.login(credentials)
      
      console.log('📥 Respuesta del backend:', response)
      console.log('📊 Status:', response.status)
      console.log('📋 Data:', response.data)
      
      // ✅ VERIFICAR QUE LA RESPUESTA SEA EXITOSA
      if (response.status === 200 && response.data) {
        console.log('✅ Login exitoso en authService')
        
        return {
          success: true,
          data: response.data
        }
      } else {
        console.log('❌ Respuesta no exitosa:', response)
        
        return {
          success: false,
          error: 'Respuesta inválida del servidor'
        }
      }
      
    } catch (error) {
      console.error('❌ Error en authService.login:', error)
      console.error('❌ Error response:', error.response?.data)
      
      return {
        success: false,
        error: error.response?.data?.detail || error.message || 'Error de conexión'
      }
    }
  },

  // Logout
  logout() {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    localStorage.removeItem('pending_email') // por si acaso quedó
  },

  // Obtener usuario actual
  async getCurrentUser() {
    try {
      const response = await authAPI.me()
      return response.data
    } catch (error) {
      throw error.response?.data || error
    }
  },

  // Verificar si está autenticado
  isAuthenticated() {
    return !!localStorage.getItem('token')
  },

  // Obtener usuario desde localStorage
  getUser() {
    const user = localStorage.getItem('user')
    return user ? JSON.parse(user) : null
  }
}

