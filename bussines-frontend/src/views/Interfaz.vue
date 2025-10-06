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
            <div class="nav-item" :class="{ active: currentSection === 'nueva' }"
              @click="startNewConversation">
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

        <!-- Botón para cambiar entre modo simple y con historial -->
        <n-tooltip :disabled="!isSidebarCollapsed" placement="right">
          <template #trigger>
            <div 
              class="nav-item mode-toggle-item" 
              @click="toggleMode"
            >
              <n-icon size="20">
                <component :is="chatStore.isSimpleMode ? ChatbubbleOutline : FolderOutline" />
              </n-icon>
              <span :class="{ 'text-hidden': isSidebarCollapsed }">
                {{ chatStore.isSimpleMode ? 'Chat Simple' : 'Con Historial' }}
              </span>
            </div>
          </template>
          {{ chatStore.isSimpleMode ? 'Chat Simple' : 'Con Historial' }}
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

        <!-- Test de conexión -->
        <n-tooltip :disabled="!isSidebarCollapsed" placement="right">
          <template #trigger>
            <div class="nav-item" @click="testConnection">
              <n-icon size="20"><FlaskOutline /></n-icon>
              <span :class="{ 'text-hidden': isSidebarCollapsed }">Test IA</span>
            </div>
          </template>
          Test IA
        </n-tooltip>
      </nav>

      <!-- Recientes section - Lista de conversaciones -->
      <div v-if="!chatStore.isSimpleMode && !isSidebarCollapsed" class="sidebar-section">
        <h3>Conversaciones</h3>
        <button 
        v-if="chatStore.conversations.length === 0" 
        @click="loadConversationsIfNeeded"
        class="load-conversations-btn"
      >
        Cargar Conversaciones
      </button>
        <div class="conversations-list">
          <div
            v-for="conv in chatStore.conversations"
            :key="conv.id"
            class="conversation-item"
            :class="{ active: chatStore.currentConversation?.id === conv.id }"
            @click="selectConversation(conv)"
          >
            <div class="conversation-info">
              <span class="conversation-title">{{ conv.title }}</span>
              <span class="conversation-date">{{ formatDate(conv.updated_at) }}</span>
            </div>
            <button 
              @click.stop="deleteConversation(conv.id)"
              class="delete-conv-btn"
            >
              🗑️
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Main content -->
    <div class="main-wrapper" :class="{ 'main-expanded': isSidebarCollapsed }">
      <header class="header">
        <div class="logo">StarNow</div>
        <!-- Indicador de modo -->
        <div class="mode-indicator">
          <span v-if="chatStore.isSimpleMode" class="mode-badge simple">
            💬 Chat Simple
          </span>
          <span v-else class="mode-badge history">
            📚 Con Historial
          </span>
        </div>
      </header>

      <main class="main-content">
        <!-- Contenido condicional -->
        <template v-if="currentSection === 'chats'">
          <div class="chat-container">
            <!-- Error Display -->
            <div v-if="chatStore.error" class="error-banner">
              ⚠️ {{ chatStore.error }}
              <button @click="chatStore.clearError()" class="error-close-btn">×</button>
            </div>

            <!-- Mensajes -->
            <div class="messages-area" ref="messagesContainer">
              <div
                v-for="message in chatStore.getCurrentMessages"
                :key="message.id"
                class="chat-message"
                :class="message.role"
              >
                <div class="message-bubble">
                  <div class="message-header">
                    <strong>{{ message.role === 'user' ? 'Tú' : 'IA Business Advisor' }}</strong>
                    <small class="message-timestamp">{{ formatTime(message.created_at) }}</small>
                  </div>
                  <div class="message-body">{{ message.content }}</div>
                </div>
              </div>

              <!-- Loading indicator -->
              <div v-if="chatStore.isLoading" class="chat-message assistant">
                <div class="message-bubble">
                  <div class="message-header">
                    <strong>IA Business Advisor</strong>
                  </div>
                  <div class="typing-animation">
                    <span></span><span></span><span></span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Input area -->
            <div class="chat-input-area">
              <div class="input-wrapper">
                <input
                  v-model="userQuery"
                  @keypress.enter="handleSubmit"
                  placeholder="Escribe tu consulta sobre tu emprendimiento..."
                  class="chat-input"
                  :disabled="chatStore.isLoading"
                />
                <button 
                  @click="handleSubmit"
                  :disabled="!userQuery.trim() || chatStore.isLoading"
                  class="send-button"
                >
                  {{ chatStore.isLoading ? '⏳' : '➤' }}
                </button>
              </div>
              <div class="input-footer">
                <button @click="clearCurrentChat" class="clear-btn">
                  🗑️ Limpiar
                </button>
                <small class="input-hint">Presiona Enter para enviar</small>
              </div>
            </div>
          </div>
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
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useMessage } from 'naive-ui'
import { useAuthStore } from '../stores/auth'
import { useChatStore } from '../stores/chat'
import { 
  ArrowForwardOutline, 
  MenuOutline,
  AddCircleOutline,
  ChatbubbleOutline,
  FolderOutline,
  CubeOutline,
  FlaskOutline
} from '@vicons/ionicons5'
import ProyectoForm from '../components/ProyectoForm.vue'
import ArtefactosPanel from '../components/ArtefactosPanel.vue'
import { chatService } from '../services/chatService'

const router = useRouter()
const message = useMessage()
const authStore = useAuthStore()
const chatStore = useChatStore()
const userQuery = ref('')
const isLoggingOut = ref(false)
const messagesContainer = ref(null)

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

// ====== FUNCIONES DE CHAT ======

// Toggle entre modo simple y con historial
const toggleMode = async () => {
  try {
    const wasSimpleMode = chatStore.isSimpleMode
    chatStore.isSimpleMode = !chatStore.isSimpleMode
    
    if (wasSimpleMode) {
      message.info('Cambiado a Modo Historial')
    } else {
      message.info('Cambiado a Chat Simple')
      chatStore.currentConversation = null
      chatStore.messages = []
    }
  } catch (error) {
    console.error('Error al cambiar modo:', error)
    message.error('Error al cambiar modo de chat')
  }
}

// Test de conexión con IA
const testConnection = async () => {
  try {
    const result = await chatService.testConnection()
    if (result.success) {
      message.success('✅ Conexión con IA exitosa')
      console.log('Test result:', result.data)
    } else {
      message.error('❌ Error en conexión: ' + result.error)
    }
  } catch (error) {
    message.error('❌ Error probando conexión')
  }
}

// Cargar conversaciones solo cuando sea necesario
// ✅ FUNCIÓN MEJORADA loadConversationsIfNeeded
const loadConversationsIfNeeded = async () => {
  // Verificar autenticación primero
  if (!authStore.isAuthenticated || !authStore.token) {
    console.error('🚨 No hay token válido')
    message.error('Sesión expirada. Inicia sesión nuevamente.')
    await router.push('/login')
    return
  }

  if (!chatStore.isSimpleMode && chatStore.conversations.length === 0) {
    try {
      console.log('🔄 Cargando conversaciones...')
      await chatStore.loadConversations()
      console.log('✅ Conversaciones cargadas')
    } catch (error) {
      console.error('❌ Error cargando conversaciones:', error)
      
      if (error.response?.status === 401) {
        message.error('Sesión expirada. Redirigiendo al login...')
        authStore.logout()
        await router.push('/login')
      } else {
        message.error('Error cargando historial de conversaciones')
      }
    }
  }
}

// ✅ FUNCIÓN ÚNICA startNewConversation
function startNewConversation() {
  if (!chatStore.isSimpleMode) {
    loadConversationsIfNeeded().then(() => {
      chatStore.createConversation()
    })
  } else {
    chatStore.clearSimpleChat()
  }
  currentSection.value = 'chats'
}

// Gestión de conversaciones
const selectConversation = async (conversation) => {
  try {
    await chatStore.selectConversation(conversation)
    currentSection.value = 'chats'
  } catch (error) {
    message.error('Error al cargar conversación')
  }
}

const deleteConversation = async (conversationId) => {
  try {
    await chatStore.deleteConversation(conversationId)
    message.success('Conversación eliminada')
  } catch (error) {
    message.error('Error al eliminar conversación')
  }
}

// Limpiar chat actual
const clearCurrentChat = () => {
  if (chatStore.isSimpleMode) {
    chatStore.clearSimpleChat()
    message.success('Chat limpiado')
  } else {
    startNewConversation()
  }
}

// Scroll al final de los mensajes
const scrollToBottom = () => {
  if (messagesContainer.value) {
    nextTick(() => {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    })
  }
}

// Formateo de fechas y horas
const formatDate = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = Math.abs(now - date)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays === 1) return 'Hoy'
  if (diffDays === 2) return 'Ayer'
  if (diffDays <= 7) return `Hace ${diffDays} días`
  return date.toLocaleDateString()
}

const formatTime = (dateString) => {
  return new Date(dateString).toLocaleTimeString('es-ES', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

// ====== FUNCIONES PRINCIPALES ======

async function handleSubmit() {
  try {
    let queryText = ''
    
    if (typeof userQuery.value === 'string') {
      queryText = userQuery.value.trim()
    } else if (userQuery.value !== null && userQuery.value !== undefined) {
      queryText = String(userQuery.value).trim()
    }
    
    if (!queryText || queryText.length === 0) {
      message.warning('Por favor escribe una pregunta')
      return
    }

    currentSection.value = 'chats'
    userQuery.value = ''

    if (chatStore.isSimpleMode) {
      await chatStore.sendSimpleMessage(queryText)
    } else {
      await chatStore.sendMessage(queryText)
    }
    
    await nextTick()
    scrollToBottom()
    
  } catch (error) {
    console.error('Error completo:', error)
    message.error('Error al enviar mensaje: ' + (error.message || 'Error desconocido'))
  }
}

const selectSuggestion = (suggestionText) => {
  userQuery.value = suggestionText
  nextTick(() => {
    handleSubmit()
  })
}

const handleLogout = async () => {
  isLoggingOut.value = true
  
  try {
    authStore.logout()
    message.success('Sesión cerrada correctamente')
    router.push('/')
  } catch (error) {
    console.error('Error al cerrar sesión:', error)
    message.error('Error al cerrar sesión')
  } finally {
    isLoggingOut.value = false
  }
}

// Cargar conversaciones al montar si está en modo historial
onMounted(() => {
  if (!chatStore.isSimpleMode) {
    loadConversationsIfNeeded()
  }
})
</script>

<style scoped>
/* ✅ ESTILOS CORREGIDOS PARA MENSAJES */

.chat-message {
  max-width: 75%;
  display: flex;
  margin-bottom: 16px;
}

.chat-message.user {
  align-self: flex-end;
}

.chat-message.assistant {
  align-self: flex-start;
}

.message-bubble {
  padding: 16px 20px;
  border-radius: 18px;
  width: 100%;
  word-wrap: break-word;
}

/* ✅ MENSAJE DEL USUARIO - Fondo morado, texto blanco */
.chat-message.user .message-bubble {
  background: linear-gradient(135deg, #a855f7 0%, #8b5cf6 100%);
  color: white;
  border: none;
}

/* ✅ MENSAJE DE LA IA - Fondo gris claro, texto negro */
.chat-message.assistant .message-bubble {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  color: #111827; /* NEGRO PARA MÁXIMA LEGIBILIDAD */
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  font-size: 13px;
  font-weight: 600;
}

/* ✅ HEADER DEL USUARIO */
.chat-message.user .message-header {
  color: rgba(255, 255, 255, 0.9);
}

.chat-message.user .message-header strong {
  color: white;
}

/* ✅ HEADER DE LA IA */
.chat-message.assistant .message-header {
  color: #4b5563;
}

.chat-message.assistant .message-header strong {
  color: #1f2937;
}

.message-body {
  line-height: 1.6;
  white-space: pre-wrap;
  font-size: 14px;
  word-wrap: break-word;
}

/* ✅ TEXTO DEL USUARIO - Blanco */
.chat-message.user .message-body {
  color: white;
}

/* ✅ TEXTO DE LA IA - Negro */
.chat-message.assistant .message-body {
  color: #111827 !important; /* IMPORTANTE: Forzar color negro */
  font-weight: 400;
}

.message-timestamp {
  font-size: 11px;
  font-weight: 400;
}

/* ✅ TIMESTAMP DEL USUARIO */
.chat-message.user .message-timestamp {
  color: rgba(255, 255, 255, 0.8);
}

/* ✅ TIMESTAMP DE LA IA */
.chat-message.assistant .message-timestamp {
  color: #6b7280;
}

/* ✅ INDICADOR DE CARGA */
.typing-animation {
  display: flex;
  gap: 4px;
  align-items: center;
  padding: 8px 0;
}

.typing-animation span {
  width: 8px;
  height: 8px;
  background: #a855f7;
  border-radius: 50%;
  animation: typing-pulse 1.4s ease-in-out infinite both;
}

.typing-animation span:nth-child(1) { animation-delay: -0.32s; }
.typing-animation span:nth-child(2) { animation-delay: -0.16s; }
.typing-animation span:nth-child(3) { animation-delay: 0; }

@keyframes typing-pulse {
  0%, 80%, 100% { 
    transform: scale(0);
    opacity: 0.5;
  }
  40% { 
    transform: scale(1);
    opacity: 1;
  }
}

/* ✅ ÁREA DE MENSAJES */
.messages-area {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  background: white;
}

/* ✅ RESTO DE TUS ESTILOS EXISTENTES... */
.interfaz {
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
  overflow-y: auto;
  color: #1e293b; /* TEXTO NEGRO EN SIDEBAR */
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
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  color: #374151; /* TEXTO GRIS OSCURO */
  transition: all 0.3s ease;
  margin-bottom: 8px;
  white-space: nowrap;
}

.nav-item:hover {
  background: #f8fafc;
  color: #1e293b; /* TEXTO NEGRO AL HOVER */
}

.nav-item.active {
  background: #ede9fe;
  color: #7c3aed; /* TEXTO MORADO AL ESTAR ACTIVO */
  border: 1px solid #c4b5fd;
}

.mode-toggle-item {
  background: rgba(168, 85, 247, 0.05);
  border: 1px solid rgba(168, 85, 247, 0.2);
}

.sidebar-section {
  padding: 16px;
  border-top: 1px solid #f0f0f0;
  flex: 1;
  overflow-y: auto;
}

.sidebar-section h3 {
  font-size: 14px;
  color: #4b5563; /* TEXTO GRIS OSCURO */
  margin-bottom: 12px;
  font-weight: 600;
  transition: opacity 0.3s ease;
}

.conversations-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.conversation-item {
  padding: 10px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.2s;
  background: #f8f9fa;
  color: #374151; /* TEXTO GRIS OSCURO */
}

.conversation-item:hover {
  background: #f1f5f9;
  color: #1e293b; /* TEXTO NEGRO AL HOVER */
}

.conversation-item.active {
  background: rgba(168, 85, 247, 0.1);
  border: 1px solid rgba(168, 85, 247, 0.3);
  color: #7c3aed; /* TEXTO MORADO AL ESTAR ACTIVO */
}

.conversation-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
  min-width: 0;
}

.conversation-title {
  font-size: 13px;
  font-weight: 500;
  color: inherit;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.conversation-date {
  font-size: 11px;
  color: #64748b;
}

.delete-conv-btn {
  background: none;
  border: none;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.2s;
  padding: 4px;
  font-size: 14px;
}

.conversation-item:hover .delete-conv-btn {
  opacity: 1;
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
  display: flex;
  flex-direction: column;
}

.main-expanded {
  margin-left: 72px;
}

.header {
  padding: 24px 32px;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
}

.logo {
  font-size: 24px;
  font-weight: 700;
  color: #1a1a1a;
  letter-spacing: -0.01em;
}

.mode-indicator {
  display: flex;
  align-items: center;
}

.mode-badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
}

.mode-badge.simple {
  background: #f1f5f9;
  color: #64748b;
}

.mode-badge.history {
  background: rgba(168, 85, 247, 0.1);
  color: #a855f7;
}

.main-content {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px 24px;
  overflow: hidden;
  background: #f8fafc;
}

/* Chat Container */
.chat-container {
  width: 100%;
  max-width: 900px;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(168, 85, 247, 0.08);
  overflow: hidden;
}

.error-banner {
  background: #fef2f2;
  color: #dc2626;
  padding: 12px 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #fecaca;
  font-size: 14px;
}

.error-close-btn {
  background: none;
  border: none;
  color: #dc2626;
  cursor: pointer;
  font-size: 20px;
  padding: 0;
}

.chat-input-area {
  border-top: 1px solid #f0f0f0;
  padding: 20px;
  background: #f8fafc;
}

.input-wrapper {
  display: flex;
  gap: 12px;
  margin-bottom: 12px;
}

.chat-input {
  flex: 1;
  padding: 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 15px;
  outline: none;
  transition: border-color 0.2s;
  color: #1e293b; /* TEXTO NEGRO EN INPUT */
  background: white;
}

.chat-input:focus {
  border-color: #a855f7;
}

.chat-input::placeholder {
  color: #94a3b8; /* PLACEHOLDER GRIS */
}

.send-button {
  padding: 12px 24px;
  background: #a855f7;
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-size: 18px;
  transition: all 0.2s;
}

.send-button:hover:not(:disabled) {
  background: #9333ea;
  transform: translateY(-1px);
}

.send-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.input-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.clear-btn {
  padding: 6px 12px;
  background: none;
  border: none;
  cursor: pointer;
  color: #64748b;
  font-size: 13px;
  transition: color 0.2s;
}

.clear-btn:hover {
  color: #1e293b;
}

.input-hint {
  color: #64748b;
  font-size: 12px;
}

.load-conversations-btn {
  padding: 8px 16px;
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  cursor: pointer;
  font-size: 12px;
  color: #64748b;
  transition: all 0.2s;
  margin-bottom: 12px;
  width: 100%;
}

.load-conversations-btn:hover {
  background: #e2e8f0;
  color: #a855f7;
}


</style>