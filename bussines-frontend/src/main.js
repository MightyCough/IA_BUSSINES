import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import naive from 'naive-ui'
import './assets/styles/main.css'


import App from './App.vue'
import routes from './router'

const router = createRouter({
    history: createWebHistory(),
    routes
})

const app = createApp(App)

app.use(router)
app.use(naive)

app.mount('#app')
