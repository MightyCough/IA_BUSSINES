import Home from '../views/LandingPage.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Interfaz from  '../views/Interfaz.vue'



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
        path: '/:pathMatch(.*)*',
        redirect: '/'
    },
    { 
        path: '/interfaz',
        name: 'Interfaz',
        component: Interfaz,
        meta: { 
            title: 'Interfaz - AI Business Advisor',
            requiresAuth: true 
        }
    }
]

export default routes