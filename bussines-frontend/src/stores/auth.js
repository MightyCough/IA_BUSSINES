import {defineStore} from 'pinia'
import {authService} from '../services/authService'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
    token: localStorage.getItem('token') || null,
    isAuthenticated: !!localStorage.getItem('token'),
    error: null,
    isLoading: false
  }),

  getters: {
    hasError: (state) => !!state.error,
    isLoggedIn: (state) => !!state.token && !!state.user
  },

  actions: {
    clearError() {
      this.error = null
    },

    setError(error) {
      this.error = error
    },

    setLoading(loading) {
      this.isLoading = loading
    },

    async login(credentials) {
      try {
        this.isLoading = true
        this.error = null
        
        console.log('🔄 Store: Intentando login...')
        
        const response = await authService.login(credentials)
        
        console.log('📥 Store: Respuesta de authService:', response)
        
        if (response.success) {
          this.user = response.data.user
          this.token = response.data.access_token
          this.isAuthenticated = true
          
          // Guardar en localStorage
          localStorage.setItem('token', this.token)
          localStorage.setItem('user', JSON.stringify(this.user))
          
          console.log('✅ Store: Login exitoso - Token guardado:', this.token.substring(0, 20) + '...')
          
          return response
        } else {
          console.log('❌ Store: Login falló:', response.error)
          this.error = response.error || 'Error en el login'
          throw new Error(this.error)
        }
      } catch (error) {
        console.error('❌ Store: Error en login:', error)
        this.error = error.message || 'Error de conexión'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    initializeAuth() {
      const token = localStorage.getItem('token')
      const user = localStorage.getItem('user')
      
      if (token && user) {
        try {
          this.token = token
          this.user = JSON.parse(user)
          this.isAuthenticated = true
          console.log('✅ Autenticación inicializada desde localStorage')
        } catch (error) {
          console.error('❌ Error parseando usuario desde localStorage:', error)
          this.logout()
        }
      }
    },

    logout() {
      this.user = null
      this.token = null
      this.isAuthenticated = false
      this.error = null
      this.isLoading = false
      
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      
      console.log('🚪 Usuario deslogueado')
    }
  }
})