import {defineStore} from 'pinia'
import {authService} from '../services/authService'

export const useAuthStore = defineStore('auth',{
    state:()=>({
        user: null,
        token: null,
        isLoading: false,
        error: null
    }),
    
    getters:{
        isAuthenticated: (state) => !!state.token,
        userName: (state) => state.user?.full_name || '',
        userEmail:(state) => state.user?.email || ''
    },

    actions: {
        //Inicializar desde localStorage
        init(){
            const token = localStorage.getItem('token')
            const user  = localStorage.getItem('user')

            if(token && user){
                this.token = token
                this.user = JSON.parse(user)
            }
        },
    
    //Registro
    async register(userData){
        this.isLoading = true
        this.error = null

        try{
            const response = await authService.register(userData)
            this.token = response.access_token
            this.user = response.user
            return response
        }catch(error){
            this.error = error.detail || 'Error en el login'
            throw error
        }finally{
            this.isLoading = false
        }
    },

    //Login
    async login(credentials) {
      this.isLoading = true
      this.error = null
      
      try {
        // Simular login por ahora (comentar cuando conectes el backend)
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        const mockResponse = {
          access_token: 'mock-token-123',
          user: {
            id: '1',
            email: credentials.email,
            full_name: 'Usuario Demo',
            business_type: 'producto',
            stage: 'idea'
          }
        }
        
        this.token = mockResponse.access_token
        this.user = mockResponse.user
        
        localStorage.setItem('token', mockResponse.access_token)
        localStorage.setItem('user', JSON.stringify(mockResponse.user))
        
        return mockResponse
      } catch (error) {
        this.error = error.detail || 'Error en el login'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    //Logout
    logout(){
        this.user = null
        this.token = null
        this.error = null
        authService.logout()
    },

    //Limpiar errores
    clearError(){
        this.error = null
    }

    }
})