import {authAPI} from './api.js'

export const authService ={
    // Registro
  async register(userData) {
    try {
      const response = await authAPI.register({
        email: userData.email,
        password: userData.password,
        full_name: userData.full_name,
        business_type: userData.business_type || 'producto',
        stage: userData.stage || 'idea'
      })
      
      // Guardar token y usuario
      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token)
        localStorage.setItem('user', JSON.stringify(response.data.user))
      }
      
      return response.data
    } catch (error) {
        console.error('Register error:', error)
        throw error.response?.data || error
    }
  },

  // Login
  async login(credentials){
    try{
        const response = await authAPI.login(credentials)

        if(response.data.access_token){
            localStorage.setItem('token',response.data.access_token)
            localStorage.setItem('user',JSON.stringify(response.data.user))
        }
        return response.data
    }catch(error){
        throw error.response?.data || error
    }
  },

  //logout
  logout(){
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  },

  //Obtener usuario actual
  async getCurrentUser(){
    try{
        const response = await authAPI.me()
        return response.data
    }catch(error){
        throw error.response?.data || error
    }
  },

  //Verificar si esta autenticado
  isAuthenticated(){
    return !!localStorage.getItem('token')
  },

  //Obtener usuario desde localStorage
  getUser(){
    const user = localStorage.getItem('user')
    return user ? JSON.parse(user) : null
  }

}