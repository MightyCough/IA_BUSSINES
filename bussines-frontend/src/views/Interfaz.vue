<template>
  <div class="interfaz">
    <!-- Sidebar -->
    <div class="sidebar" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
      <!-- Toggle button -->
      <button class="sidebar-toggle" @click="toggleSidebar">
        <n-icon size="20">
          <MenuOutline />
        </n-icon>
      </button>

      <!-- Logo section -->
      <div class="sidebar-logo">
        <span class="logo-text" :class="{ 'text-hidden': isSidebarCollapsed }">StarNow</span>
      </div>

      <!-- Navigation items -->
      <nav class="sidebar-nav">
        <n-tooltip :disabled="!isSidebarCollapsed" placement="right">
          <template #trigger>
            <div class="nav-item" :class="{ active: currentSection === 'nueva' }">
              <n-icon size="20"><AddCircleOutline /></n-icon>
              <span :class="{ 'text-hidden': isSidebarCollapsed }">Nueva conversación</span>
            </div>
          </template>
          Nueva conversación
        </n-tooltip>

        <n-tooltip :disabled="!isSidebarCollapsed" placement="right">
          <template #trigger>
            <div 
              class="nav-item" 
              :class="{ active: currentSection === 'chats' }"
              @click="currentSection = 'chats'"
            >
              <n-icon size="20"><ChatbubbleOutline /></n-icon>
              <span :class="{ 'text-hidden': isSidebarCollapsed }">Chats</span>
            </div>
          </template>
          Chats
        </n-tooltip>

        <n-tooltip :disabled="!isSidebarCollapsed" placement="right">
          <template #trigger>
            <div class="nav-item" :class="{ active: currentSection === 'proyectos' }" @click="currentSection = 'proyectos'">
              <n-icon size="20"><FolderOutline /></n-icon>
              <span :class="{ 'text-hidden': isSidebarCollapsed }">Proyectos</span>
            </div>
          </template>
          Proyectos
        </n-tooltip>

        <n-tooltip :disabled="!isSidebarCollapsed" placement="right">
          <template #trigger>
            <div class="nav-item" :class="{ active: currentSection === 'artefactos' }" @click="currentSection = 'artefactos'">
              <n-icon size="20"><CubeOutline /></n-icon>
              <span :class="{ 'text-hidden': isSidebarCollapsed }">Artefactos</span>
            </div>
          </template>
          Artefactos
        </n-tooltip>
      </nav>

      <!-- Recientes section -->
      <div class="sidebar-section">
        <h3 :class="{ 'text-hidden': isSidebarCollapsed }">Recientes</h3>
        <!-- Aquí puedes añadir la lista de conversaciones recientes -->
      </div>
    </div>

    <!-- Main content -->
    <div class="main-wrapper" :class="{ 'main-expanded': isSidebarCollapsed }">
      <header class="header">
        <div class="logo">StarNow</div>
      </header>

      <main class="main-content">
        <!-- Contenido condicional -->
        <template v-if="currentSection === 'chats'">
          <ChatView />
        </template>
        <template v-else-if="currentSection === 'proyectos'">
          <ProyectoForm />
        </template>
        <template v-else-if="currentSection === 'artefactos'">
          <ArtefactosPanel />
        </template>
        <template v-else>
          <div class="container">
            <!-- Título principal -->
            <h1 class="main-title">¿Por dónde iniciamos hoy?</h1>
            <!-- Input de consulta -->
            <div class="input-section">
              <n-input
                v-model:value="userQuery"
                size="large"
                placeholder="Escribe tu consulta sobre tu emprendimiento"
                class="query-input"
                @keyup.enter="handleSubmit"
              />
            </div>
            <!-- Botón de envío (opcional, aparece cuando hay texto) -->
            <div v-if="userQuery.trim()" class="submit-section">
              <n-button 
                type="primary" 
                size="large"
                round
                class="submit-button"
                @click="handleSubmit"
              >
                Comenzar conversación
                <template #icon>
                  <n-icon>
                    <ArrowForwardOutline />
                  </n-icon>
                </template>
              </n-button>
            </div>
            <!-- Sugerencias rápidas (opcional) -->
            <div class="suggestions">
              <div class="suggestions-title">O elige una opción:</div>
              <div class="suggestion-chips">
                <n-tag 
                  v-for="suggestion in suggestions" 
                  :key="suggestion.id"
                  clickable
                  round
                  class="suggestion-chip"
                  @click="selectSuggestion(suggestion.text)"
                >
                  {{ suggestion.text }}
                </n-tag>
              </div>
            </div>
            <!-- Añadir el botón de logout donde quieras en tu diseño actual -->
            <div class="logout-section">
              <n-button 
                type="error" 
                size="large"
                @click="handleLogout"
                :loading="isLoggingOut"
              >
                {{ isLoggingOut ? 'Cerrando sesión...' : 'Cerrar Sesión' }}
              </n-button>
            </div>
          </div>
        </template>

      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useMessage } from 'naive-ui'
import { useAuthStore } from '../stores/auth'
import { 
  ArrowForwardOutline, 
  MenuOutline,
  AddCircleOutline,
  ChatbubbleOutline,
  FolderOutline,
  CubeOutline
} from '@vicons/ionicons5'
import ChatView from '../components/ChatView.vue'

import ProyectoForm from '../components/ProyectoForm.vue'
import ArtefactosPanel from '../components/ArtefactosPanel.vue'

const router = useRouter()
const message = useMessage()
const authStore = useAuthStore()
const userQuery = ref('')
const isLoggingOut = ref(false)

// Sugerencias predefinidas
const suggestions = ref([
  { id: 1, text: 'Validar mi idea de negocio' },
  { id: 2, text: 'Crear un plan de negocio' },
  { id: 3, text: 'Estrategias de marketing' },
  { id: 4, text: 'Análisis de competencia' },
  { id: 5, text: 'Modelos de monetización' }
])

const isSidebarCollapsed = ref(false)
const currentSection = ref('nueva')

const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}

// Métodos
const handleSubmit = () => {
  if (userQuery.value.trim()) {
    console.log('Consulta enviada:', userQuery.value)
    // Aquí irá la lógica para procesar la consulta con IA
    
    // Por ahora, simulamos ir a una página de chat
    // router.push('/chat')
  }
}

const selectSuggestion = (suggestionText) => {
  userQuery.value = suggestionText
  handleSubmit()
}

const handleLogout = async () => {
  isLoggingOut.value = true
  
  try {
    // Cerrar sesión
    authStore.logout()
    
    // Mostrar mensaje de éxito
    message.success('Sesión cerrada correctamente')
    
    // Redirigir a la página principal
    router.push('/')
    
  } catch (error) {
    console.error('Error al cerrar sesión:', error)
    message.error('Error al cerrar sesión')
  } finally {
    isLoggingOut.value = false
  }
}
</script>

<style scoped>
.interfaz {
.proyecto-form-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 70vh;
}

.proyecto-form-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(168, 85, 247, 0.08), 0 1.5px 6px rgba(0,0,0,0.03);
  padding: 40px 32px;
  max-width: 480px;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 28px;
}

.proyecto-form-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.proyecto-label {
  font-size: 15px;
  font-weight: 600;
  color: #6b7280;
}

.proyecto-input,
.proyecto-textarea {
  --n-border-radius: 10px;
  --n-font-size: 16px;
  --n-border: 2px solid #e6e6e6;
  --n-border-focus: 2px solid #a855f7;
  --n-border-hover: 2px solid #a855f7;
  --n-padding-left: 18px;
  --n-padding-right: 18px;
}

.proyecto-textarea {
  min-height: 80px;
}

.proyecto-form-actions {
  display: flex;
  justify-content: flex-end;
}

.proyecto-submit {
  background: linear-gradient(135deg, #a855f7 0%, #8b5cf6 100%);
  border: none;
  font-weight: 600;
  font-size: 16px;
  box-shadow: 0 4px 14px rgba(168, 85, 247, 0.13);
  transition: all 0.3s ease;
}
.proyecto-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
  display: flex;
  min-height: 100vh;
  background: #ffffff;
}

.sidebar {
  width: 260px;
  background: #ffffff;
  border-right: 1px solid #f0f0f0;
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  transition: width 0.3s ease;
  display: flex;
  flex-direction: column;
  z-index: 100;
}

.sidebar-collapsed {
  width: 72px;
}

.sidebar-toggle {
  position: absolute;
  right: -12px;
  top: 24px;
  width: 24px;
  height: 24px;
  background: white;
  border: 1px solid #f0f0f0;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #666;
  z-index: 2;
  transition: all 0.3s ease;
}

.sidebar-toggle:hover {
  background: #f5f5f5;
  color: #a855f7;
}

.sidebar-logo {
  padding: 24px;
  border-bottom: 1px solid #f0f0f0;
}

.logo-text {
  font-size: 24px;
  font-weight: 700;
  background: linear-gradient(135deg, #a855f7 0%, #8b5cf6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  transition: opacity 0.3s ease;
}

.sidebar-nav {
  padding: 24px 16px;
  flex: 1;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  color: #666;
  transition: all 0.3s ease;
  margin-bottom: 8px;
  white-space: nowrap;
}

.nav-item:hover {
  background: #f5f5f5;
  color: #a855f7;
}

.nav-item.active {
  background: rgba(168, 85, 247, 0.1);
  color: #a855f7;
}

.sidebar-section {
  padding: 24px 16px;
  border-top: 1px solid #f0f0f0;
}

.sidebar-section h3 {
  font-size: 14px;
  color: #666;
  margin-bottom: 16px;
  font-weight: 600;
  transition: opacity 0.3s ease;
}

.text-hidden {
  opacity: 0;
  width: 0;
  overflow: hidden;
}

.main-wrapper {
  flex: 1;
  margin-left: 260px;
  transition: margin-left 0.3s ease;
}

.main-expanded {
  margin-left: 72px;
}

/* Header */
.header {
  padding: 24px 32px;
  border-bottom: 1px solid #f0f0f0;
}

.logo {
  font-size: 24px;
  font-weight: 700;
  color: #1a1a1a;
  letter-spacing: -0.01em;
}

/* Contenido principal */
.main-content {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px 24px;
}

.container {
  width: 100%;
  max-width: 800px;
  text-align: center;
}

/* Título principal */
.main-title {
  font-size: 2.5rem;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 60px 0;
  line-height: 1.2;
  letter-spacing: -0.02em;
}

/* Sección del input */
.input-section {
  margin-bottom: 32px;
}

.query-input {
  --n-border-radius: 32px;
  --n-height: 64px;
  --n-font-size: 16px;
  --n-border: 2px solid #e6e6e6;
  --n-border-focus: 2px solid #a855f7;
  --n-border-hover: 2px solid #a855f7;
  --n-padding-left: 24px;
  --n-padding-right: 24px;
}

/* Botón de envío */
.submit-section {
  margin-bottom: 48px;
}

.submit-button {
  background: linear-gradient(135deg, #a855f7 0%, #8b5cf6 100%);
  border: none;
  padding: 16px 32px;
  font-size: 16px;
  font-weight: 600;
  height: auto;
  box-shadow: 0 4px 14px rgba(168, 85, 247, 0.3);
  transition: all 0.3s ease;
}

.submit-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(168, 85, 247, 0.4);
}

/* Sugerencias */
.suggestions {
  margin-top: 60px;
}

.suggestions-title {
  font-size: 16px;
  color: #666;
  margin-bottom: 24px;
  font-weight: 500;
}

.suggestion-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: center;
  max-width: 600px;
  margin: 0 auto;
}

.suggestion-chip {
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  color: #495057;
  padding: 8px 16px;
  font-size: 14px;
  transition: all 0.2s ease;
  cursor: pointer;
}

.suggestion-chip:hover {
  background: #a855f7;
  border-color: #a855f7;
  color: white;
  transform: translateY(-1px);
}

/* Logout */
.logout-section {
  margin: 2rem 0;
  text-align: center;
}

/* Responsive Design */
@media (max-width: 768px) {
  .header {
    padding: 20px 24px;
  }
  
  .main-content {
    padding: 40px 20px;
  }
  
  .main-title {
    font-size: 2rem;
    margin-bottom: 40px;
  }
  
  .query-input {
    --n-height: 56px;
    --n-font-size: 15px;
  }
  
  .suggestion-chips {
    max-width: 100%;
  }
  
  .suggestion-chip {
    font-size: 13px;
    padding: 6px 12px;
  }
}

@media (max-width: 480px) {
  .header {
    padding: 16px 20px;
  }
  
  .logo {
    font-size: 20px;
  }
  
  .main-content {
    padding: 32px 16px;
  }
  
  .main-title {
    font-size: 1.75rem;
    margin-bottom: 32px;
  }
  
  .query-input {
    --n-height: 52px;
    --n-font-size: 14px;
    --n-padding-left: 20px;
    --n-padding-right: 20px;
  }
}
</style>