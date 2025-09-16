<template>
  <div class="landing">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-container">
        <!-- Badge superior -->
        <n-tag 
          type="info" 
          size="large" 
          round
          class="hero-badge"
        >
          IA especializada para emprendedores
        </n-tag>

        <!-- Título principal -->
        <h1 class="hero-title">
          Tu asesor de<br>
          Negocios <span class="highlight">inteligente</span>
        </h1>

        <!-- Subtítulo -->
        <p class="hero-subtitle">
          Desde la idea hasta la expansión. Recibe asesoría personalizada, planes de negocio 
          guiados y estrategias de crecimiento adaptadas a tu emprendimiento.
        </p>

        <!-- Cards de proceso (ahora clickeables) -->
        <div class="process-cards">
          <n-card 
            v-for="step in processSteps" 
            :key="step.id"
            hoverable
            class="process-card clickable-card"
            @click="redirectToRegister"
          >
            <div class="process-content">
              <div class="process-icon">
                <n-icon size="40" :color="step.iconColor">
                  <component :is="step.icon" />
                </n-icon>
              </div>
              <h3 class="process-title">{{ step.title }}</h3>
              <p class="process-description">{{ step.description }}</p>
              
              <!-- ✅ NUEVO: Overlay con CTA -->
              <div class="card-overlay">
                <span class="card-cta">¡Comienza ahora!</span>
              </div>
            </div>
          </n-card>
        </div>

        <!-- CTA Button -->
        <div class="cta-section">
          <n-button 
            type="primary" 
            size="large"
            round
            class="cta-button"
            @click="$router.push('/register')"
          >
            Comenzar ahora
            <template #icon>
              <n-icon>
                <ArrowForwardOutline />
              </n-icon>
            </template>
          </n-button>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { 
  BulbOutline, 
  ConstructOutline, 
  RocketOutline,
  ArrowForwardOutline 
} from '@vicons/ionicons5'

const router = useRouter()

const processSteps = ref([
  {
    id: 1,
    title: 'Ya tienes tu idea',
    description: 'Valida y desarrolla tu concepto',
    icon: BulbOutline,
    iconColor: '#f39c12'
  },
  {
    id: 2,
    title: 'Consolidar tu idea',
    description: 'Estructura y escala tu proyecto',
    icon: ConstructOutline,
    iconColor: '#3498db'
  },
  {
    id: 3,
    title: 'Empezar de cero',
    description: 'Genera ideas y encuentra oportunidades',
    icon: RocketOutline,
    iconColor: '#e74c3c'
  }
])

// ✅ NUEVO: Función para redirigir al registro
const redirectToRegister = () => {
  router.push('/register')
}
</script>

<style scoped>
.landing {
  min-height: 100vh;
  background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
}

.hero {
  padding: 60px 24px 120px 24px;
  text-align: center;
}

.hero-container {
  max-width: 1200px;
  margin: 0 auto;
}

.hero-badge {
  margin-bottom: 32px;
  font-size: 14px;
  font-weight: 500;
  background: linear-gradient(135deg, #a855f7 0%, #8b5cf6 100%);
  color: white;
  border: none;
  padding: 8px 20px;
}

.hero-title {
  font-size: 4rem;
  font-weight: 700;
  line-height: 1.1;
  color: #1a1a1a;
  margin: 0 0 24px 0;
  letter-spacing: -0.02em;
}

.highlight {
  background: linear-gradient(135deg, #a855f7 0%, #8b5cf6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.125rem;
  line-height: 1.7;
  color: #4a5568;
  max-width: 680px;
  margin: 0 auto 60px auto;
  font-weight: 400;
}

.process-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 60px;
  max-width: 1000px;
  margin-left: auto;
  margin-right: auto;
}

.process-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  transition: all 0.3s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
}

.process-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  border-color: #a855f7;
}

/* ✅ NUEVO: Estilos para cards clickeables */
.clickable-card {
  cursor: pointer;
}

.clickable-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 30px rgba(168, 85, 247, 0.3);
  border-color: #a855f7;
}

.card-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(168, 85, 247, 0.9), rgba(139, 92, 246, 0.9));
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.clickable-card:hover .card-overlay {
  opacity: 1;
}

.card-cta {
  color: white;
  font-size: 1.2rem;
  font-weight: 700;
  text-align: center;
  transform: translateY(15px);
  transition: transform 0.3s ease;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.clickable-card:hover .card-cta {
  transform: translateY(0);
}

.process-content {
  padding: 32px 24px;
  text-align: center;
  position: relative;
}

.process-icon {
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
}

.process-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 12px 0;
}

.process-description {
  font-size: 0.95rem;
  color: #64748b;
  line-height: 1.6;
  margin: 0;
}

.cta-section {
  margin-top: 48px;
}

.cta-button {
  background: linear-gradient(135deg, #a855f7 0%, #8b5cf6 100%);
  border: none;
  padding: 16px 32px;
  font-size: 16px;
  font-weight: 600;
  height: auto;
  box-shadow: 0 4px 14px rgba(168, 85, 247, 0.4);
  transition: all 0.3s ease;
}

.cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(168, 85, 247, 0.5);
}

/* Responsive Design */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-subtitle {
    font-size: 1rem;
    padding: 0 16px;
  }
  
  .process-cards {
    grid-template-columns: 1fr;
    gap: 16px;
    margin-bottom: 40px;
  }
  
  .process-content {
    padding: 24px 20px;
  }
  
  .card-cta {
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .hero {
    padding: 40px 16px 80px 16px;
  }
  
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-badge {
    font-size: 12px;
    padding: 6px 16px;
  }
  
  .card-cta {
    font-size: 0.9rem;
  }
}
</style>