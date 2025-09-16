<template>
  <div class="interfaz">
    <!-- Header con logo -->
    <header class="header">
      <div class="logo">StarNow</div>
    </header>

    <!-- Contenido principal -->
    <main class="main-content">
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
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowForwardOutline } from '@vicons/ionicons5'

const router = useRouter()
const userQuery = ref('')

// Sugerencias predefinidas
const suggestions = ref([
  { id: 1, text: 'Validar mi idea de negocio' },
  { id: 2, text: 'Crear un plan de negocio' },
  { id: 3, text: 'Estrategias de marketing' },
  { id: 4, text: 'Análisis de competencia' },
  { id: 5, text: 'Modelos de monetización' }
])

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
</script>

<style scoped>
.interfaz {
  min-height: 100vh;
  background: #ffffff;
  display: flex;
  flex-direction: column;
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