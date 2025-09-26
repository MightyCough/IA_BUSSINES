<!-- filepath: /home/mightycough/Desktop/IA_bussines/bussines-frontend/src/views/Interfaz.vue -->
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
import ProjectsView from '../components/ProjectsView.vue' // ✅ NUEVA IMPORTACIÓN

const router = useRouter()
const message = useMessage()
const authStore = useAuthStore()

// Estado de la interfaz
const isSidebarCollapsed = ref(false)
const currentSection = ref('nueva')

// Funciones
const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}

// ✅ AÑADIR FUNCIÓN PARA MANEJAR NAVEGACIÓN
const handleNavigation = (section) => {
  currentSection.value = section
}
</script>

<template>
  <div class="interfaz">
    <!-- Sidebar -->
    <div class="sidebar" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
      <!-- ...existing sidebar code... -->

      <!-- Navigation items -->
      <nav class="sidebar-nav">
        <n-tooltip :disabled="!isSidebarCollapsed" placement="right">
          <template #trigger>
            <div 
              class="nav-item" 
              :class="{ active: currentSection === 'nueva' }"
              @click="handleNavigation('nueva')"
            >
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
              @click="handleNavigation('chats')"
            >
              <n-icon size="20"><ChatbubbleOutline /></n-icon>
              <span :class="{ 'text-hidden': isSidebarCollapsed }">Chats</span>
            </div>
          </template>
          Chats
        </n-tooltip>

        <!-- ✅ PROYECTOS CON FUNCIONALIDAD -->
        <n-tooltip :disabled="!isSidebarCollapsed" placement="right">
          <template #trigger>
            <div 
              class="nav-item" 
              :class="{ active: currentSection === 'proyectos' }"
              @click="handleNavigation('proyectos')"
            >
              <n-icon size="20"><FolderOutline /></n-icon>
              <span :class="{ 'text-hidden': isSidebarCollapsed }">Proyectos</span>
            </div>
          </template>
          Proyectos
        </n-tooltip>

        <n-tooltip :disabled="!isSidebarCollapsed" placement="right">
          <template #trigger>
            <div 
              class="nav-item" 
              :class="{ active: currentSection === 'artefactos' }"
              @click="handleNavigation('artefactos')"
            >
              <n-icon size="20"><CubeOutline /></n-icon>
              <span :class="{ 'text-hidden': isSidebarCollapsed }">Artefactos</span>
            </div>
          </template>
          Artefactos
        </n-tooltip>
      </nav>

      <!-- ...existing sidebar code... -->
    </div>

    <!-- Main content -->
    <div class="main-wrapper" :class="{ 'main-expanded': isSidebarCollapsed }">
      <header class="header">
        <div class="logo">StarNow</div>
      </header>

      <main class="main-content">
        <!-- ✅ CONTENIDO CONDICIONAL ACTUALIZADO -->
        <template v-if="currentSection === 'chats'">
          <ChatView />
        </template>
        <template v-else-if="currentSection === 'proyectos'">
          <ProjectsView />
        </template>
        <template v-else-if="currentSection === 'artefactos'">
          <div class="coming-soon">
            <h2>🎯 Artefactos</h2>
            <p>Esta funcionalidad estará disponible pronto...</p>
          </div>
        </template>
        <template v-else>
          <!-- Contenido de "nueva conversación" (existente) -->
          <div class="container">
            <!-- ...existing new conversation content... -->
          </div>
        </template>
      </main>
    </div>
  </div>
</template>

<!-- ✅ AÑADIR ESTILO PARA COMING SOON -->
<style scoped>
/* ...existing styles... */

.coming-soon {
  text-align: center;
  padding: 4rem 2rem;
  color: #6b7280;
}

.coming-soon h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: #1a1a1a;
}

/* ...existing styles... */
</style>