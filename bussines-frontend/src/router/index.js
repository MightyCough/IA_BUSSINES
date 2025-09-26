import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import Home from '../views/LandingPage.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Interfaz from '../views/Interfaz.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home,
        meta: {
            title: 'AI Business Advisor - Tu mentor empresarial',
            requiresAuth: false
        }
    },
    {
        path: '/login',
        name: 'Login',
        component: Login,
        meta: { 
            title: 'Iniciar Sesión',
            requiresAuth: false 
        }
    },
    {
        path: '/register',
        name: 'Register',
        component: Register,
        meta: { 
            title: 'Crear Cuenta',
            requiresAuth: false 
        }
    },
    {
        path: '/interfaz',
        name: 'Interfaz',
        component: Interfaz,
        meta: { 
            title: 'Interfaz - AI Business Advisor',
            requiresAuth: true 
        }
    },
    {
        path: '/:pathMatch(.*)*',
        redirect: '/'
    }
]


const router = createRouter({
    history: createWebHistory(),
    routes
})

// ✅ NAVIGATION GUARDS - PROTECCIÓN DE RUTAS
router.beforeEach(async (to, from, next) => {
    // Cambiar título de la página
    if (to.meta.title) {
        document.title = to.meta.title
    }

    // Verificar autenticación
    const token = localStorage.getItem('token')
    const requiresAuth = to.meta.requiresAuth

    if (requiresAuth && !token) {
        // Ruta protegida sin token - redirigir a login
        console.log('🔒 Ruta protegida - Redirigiendo a login')
        next('/login')
    } else if ((to.name === 'Login' || to.name === 'Register') && token) {
        // Ya autenticado - redirigir a interfaz
        console.log('✅ Ya autenticado - Redirigiendo a interfaz')
        next('/interfaz')
    } else {
        next()
    }
})

export default router