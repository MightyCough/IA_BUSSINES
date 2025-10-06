import { createApp } from 'vue'
import { createPinia } from 'pinia'
import naive from 'naive-ui'
import App from './App.vue'
import router from './router'
import './style.css'


const app = createApp(App)
const pinia = createPinia()

// Use plugins
app.use(pinia)
app.use(router)
app.use(naive)

app.mount('#app')

import { useAuthStore } from './stores/auth'
const authStore = useAuthStore()
authStore.initializeAuth()
