<template>
  <div class="landing">
    <div class="navbar-wrapper">
      <Navbar />
    </div>
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

    <!-- Features Section -->
    <section id="features" class="features">
      <div class="features-container">
        <h2 class="features-title">Todo lo que necesitas para emprender</h2>
        <p class="features-subtitle">Herramientas inteligentes que se adaptan a tu etapa y tipo de negocio</p>
        
        <div class="features-grid">
          <!-- Feature Cards -->
          <div class="feature-card">
            <div class="feature-icon">
              <n-icon size="32" color="#a855f7">
                <BulbOutline />
              </n-icon>
            </div>
            <h3>Generacion de ideas</h3>
            <p>Sugerencias personalizadas según tendencias del mercado y tus recursos disponibles</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <n-icon size="32" color="#a855f7">
                <DocumentTextOutline />
              </n-icon>
            </div>
            <h3>Plan de Negocio Guiado</h3>
            <p>Canvas, Lean Startup, análisis SWOT y más herramientas con explicaciones paso a paso</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <n-icon size="32" color="#a855f7">
                <MegaphoneOutline />
              </n-icon>
            </div>
            <h3>Asesoría en Marketing</h3>
            <p>Estrategias para redes sociales, publicidad digital y posicionamiento SEO</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <n-icon size="32" color="#a855f7">
                <WalletOutline />
              </n-icon>
            </div>
            <h3>Gestion Financiera</h3>
            <p>Proyecciones simples, punto de equilibrio y análisis de costos básicos</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <n-icon size="32" color="#a855f7">
                <SchoolOutline />
              </n-icon>
            </div>
            <h3>Capacitacion Continua</h3>
            <p>Aprendizaje virtual, recursos y métricas con lenguaje sencillo y ejemplos prácticos</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <n-icon size="32" color="#a855f7">
                <TrendingUpOutline />
              </n-icon>
            </div>
            <h3>Seguimiento de Progreso</h3>
            <p>Herramientas inteligentes y métricas de avance para mantener tu momentum</p>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works Section -->
    <section id="how-it-works" class="how-it-works">
      <div class="how-it-works-container">
        <h2 class="how-it-works-title">Como funciona</h2>
        <p class="how-it-works-subtitle">Un proceso simple y efectivo para hacer crecer tu negocio</p>

        <div class="steps-container">
          <!-- Step 1 -->
          <div class="step-card">
            <div class="step-number">1</div>
            <div class="step-info">
              <h3>Registro y perfil</h3>
              <p>Registrate e indica en que etapa se encuentra tu emprendimiento</p>
            </div>
            <div class="step-options-wrapper">
              <div class="option">Ya tiene la idea</div>
              <div class="option">Consolidar la idea</div>
              <div class="option">Empezar de cero</div>
            </div>
          </div>

          <!-- Step 2 -->
          <div class="step-card">
            <div class="step-number">2</div>
            <div class="step-content">
              <div class="interaction-layout">
                <div class="chat-demo">
                  <div class="chat-message">
                    <p class="user-message">Emprendedor: "Tengo $1000 y quiero empezar un negocio de delivery de postres caseros."</p>
                    <p class="ai-message">IA: "Excelente. Con ese capital puedes empezar con un modelo pequeño. Paso 1: Define tu público objetivo..."</p>
                  </div>
                </div>
                <div class="interaction-info">
                  <h3>Interaccion inteligente</h3>
                  <p>Conversa con la IA como si fuera tu asesor personal. Recibe respuestas específicas, ejemplos prácticos y plantillas personalizadas para tu situación.</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Step 3 -->
          <div class="step-card">
            <div class="step-number">3</div>
            <div class="step-content">
              <div class="tracking-layout">
                <div class="tracking-info">
                  <h3>Seguimiento continuo</h3>
                  <p>La IA guarda tu progreso y ajusta las recomendaciones según tu avance y resultados.</p>
                </div>
                <div class="progress-items">
                  <div class="progress-item">
                    <span class="check-icon">○</span>
                    <span>Validacion de mercado</span>
                  </div>
                  <div class="progress-item">
                    <span class="check-icon">○</span>
                    <span>Plan financiero básico</span>
                  </div>
                  <div class="progress-item">
                    <span class="check-icon">○</span>
                    <span>Estrategia de marketing</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Testimonials Section -->
    <section id="testimonials" class="testimonials">
      <div class="testimonials-container">
        <h2 class="testimonials-title">Lo que dicen nuestros emprendedores</h2>
        
        <div class="testimonials-grid">
          <!-- Testimonial 1 -->
          <div class="testimonial-card">
            <div class="testimonial-header">
              <div class="avatar" style="background: #a855f7">M</div>
              <div class="user-info">
                <h4>Maria Gonzales</h4>
                <span>Reposteria artesanal</span>
              </div>
            </div>
            <p class="testimonial-text">
              "En 3 meses pasé de tener solo una idea a facturar mis primeros $5000. La IA me ayudó a estructurar todo paso a paso."
            </p>
          </div>

          <!-- Testimonial 2 -->
          <div class="testimonial-card">
            <div class="testimonial-header">
              <div class="avatar" style="background: #8b5cf6">C</div>
              <div class="user-info">
                <h4>Carlos Espinoza</h4>
                <span>Consultoria digital</span>
              </div>
            </div>
            <p class="testimonial-text">
              "Lo mejor es que habla mi idioma. Nada de términos complicados, solo consejos prácticos que puedo aplicar inmediatamente."
            </p>
          </div>

          <!-- Testimonial 3 -->
          <div class="testimonial-card">
            <div class="testimonial-header">
              <div class="avatar" style="background: #6366f1">A</div>
              <div class="user-info">
                <h4>Ana Rodriguez</h4>
                <span>E-commerce de Moda</span>
              </div>
            </div>
            <p class="testimonial-text">
              "Me ayudó a identificar errores en mi estrategia de marketing que me estaban costando clientes. Ahora mis ventas crecen 20% mensual."
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Final CTA Section -->
    <section class="final-cta">
      <div class="final-cta-container">
        <h2 class="final-cta-title">Listo para hacer crecer tu negocio</h2>
        <p class="final-cta-subtitle">
          Únete a miles de emprendedores que ya están transformando sus ideas en negocios exitosos con la ayuda de nuestra IA especializada.
        </p>
        <n-button 
          type="primary" 
          size="large"
          round
          class="final-cta-button"
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
    </section>
  </div>
</template>

<script setup>
import Navbar from '../components/Navbar.vue' // Importar el componente
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { NTag, NCard, NIcon, NButton } from 'naive-ui'
import { 
  BulbOutline, 
  ConstructOutline, 
  RocketOutline,
  ArrowForwardOutline,
  DocumentTextOutline,
  MegaphoneOutline,
  WalletOutline,
  SchoolOutline,
  TrendingUpOutline
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
.navbar-wrapper {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.landing {
  padding-top: 64px; /* Adjust this value according to your navbar height */
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

/* Features Section */
.features {
  padding: 80px 24px;
  background: #f8fafc;
}

.features-container {
  max-width: 1200px;
  margin: 0 auto;
}

.features-title {
  font-size: 2.5rem;
  font-weight: 700;
  text-align: center;
  color: #1a1a1a;
  margin-bottom: 16px;
}

.features-subtitle {
  font-size: 1.25rem;
  text-align: center;
  color: #4a5568;
  margin-bottom: 64px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 32px;
}

.feature-card {
  background: white;
  padding: 32px;
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
}

.feature-card h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 12px;
}

.feature-card p {
  font-size: 1rem;
  color: #4a5568;
  line-height: 1.6;
}

.feature-icon {
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 64px;
  height: 64px;
  background: rgba(168, 85, 247, 0.1);
  border-radius: 16px;
  margin-left: auto;
  margin-right: auto;
}

.feature-card:hover .feature-icon {
  background: rgba(168, 85, 247, 0.2);
  transform: scale(1.1);
  transition: all 0.3s ease;
}

/* How It Works Section */
.how-it-works {
  padding: 80px 24px;
  background: white;
}

.how-it-works-container {
  max-width: 1200px;
  margin: 0 auto;
}

.how-it-works-title {
  font-size: 3rem;
  font-weight: 800;
  text-align: center;
  color: #1a1a1a;
  margin-bottom: 16px;
}

.how-it-works-subtitle {
  font-size: 1.25rem;
  text-align: center;
  color: #4a5568;
  margin-bottom: 64px;
}

.steps-container {
  display: flex;
  flex-direction: column;
  gap: 48px;
}

.step-card {
  display: flex;
  align-items: flex-start;
  gap: 24px;
  padding: 32px;
  background: #ffffff;
  border-radius: 24px;
  position: relative;
  margin-top: 20px; /* Agregado para bajar todo el card */
}

.step-number {
  width: 48px;
  height: 48px;
  background: #a855f7;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 700;
  position: absolute;
  top: 110px;
  left: 150px;
  z-index: 1;
}

/* Estilo específico solo para el número del segundo paso */
.step-card:nth-child(2) .step-number {
  left: auto;
  right: 450px;
  top: 70px; /* Ajusta este valor según la posición del título */
}

/* Estilo específico para el número 3 */
.step-card:nth-child(3) .step-number {
  top: 70px;
  left: auto;
  right: 1040px;
}

.step-info {
  flex: 1;
  min-width: 300px;
  display: flex;
  flex-direction: column;
  justify-content: center; /* Centra verticalmente */
  align-items: center; /* Centra horizontalmente */
  text-align: center; /* Centra el texto */
  padding: 20px;
  padding-top: 60px; /* Aumentado para más espacio desde el número */
  position: relative;
}

.step-info h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 16px;
}

.step-info p {
  color: #4a5568;
  line-height: 1.6;
  max-width: 80%; /* Limita el ancho del texto para mejor legibilidad */
}

.step-content {
  flex: 1;
}

.step-content h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 12px;
}

.step-content p {
  color: #4a5568;
  margin-bottom: 24px;
}

.step-layout {
  display: flex;
  gap: 48px;
  align-items: flex-start;
}

.step-options-wrapper {
  flex: 1;
  background: #f8fafc;
  padding: 24px;
  border-radius: 24px;
  min-width: 300px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.option {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  margin-bottom: 8px;
  background: f8fafc;
  border-radius: 12px;
  color: #4a5568;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  border: none;
}

.option::before {
  content: "";
  width: 12px;
  height: 12px;
  background: #a855f7;
  border-radius: 50%;
  margin-right: 12px;
  opacity: 0.5;
}

.option:hover {
  transform: translateX(4px);
  background: #f8fafc;
}

.option:last-child {
  margin-bottom: 0;
}

.option:hover::before {
  opacity: 1;
}

.interaction-layout {
  display: flex;
  gap: 48px;
  align-items: flex-start;
}

.interaction-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center; /* Centra horizontalmente */
  text-align: center; /* Centra el texto */
  padding: 20px;
  min-width: 300px;
  position: relative;
}

.interaction-info h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.interaction-info p {
  color: #4a5568;
  line-height: 1.6;
  max-width: 80%; /* Limita el ancho del texto para mejor legibilidad */
  margin: 0 auto; /* Centra el párrafo */
}

.chat-demo {
  flex: 1;
  background: #f8fafc;
  padding: 24px;
  border-radius: 16px;
  min-width: 300px;
}

.chat-message .user-message {
  background: white;
  padding: 16px;
  border-radius: 12px;
  margin-bottom: 12px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.chat-message .ai-message {
  background: #a855f7;
  color: white;
  padding: 16px;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.tracking-layout {
  display: flex;
  gap: 48px;
  align-items: flex-start;
}

.tracking-info {
  flex: 1;
  min-width: 300px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 20px;
  position: relative;
}

.tracking-info h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 16px;
}

.tracking-info p {
  color: #4a5568;
  line-height: 1.6;
  max-width: 80%;
  margin: 0 auto;
}

.progress-items {
  flex: 1;
  background: #f8fafc;
  padding: 24px;
  border-radius: 16px;
  min-width: 300px;
}

.progress-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: white;
  border-radius: 8px;
  margin-bottom: 12px;
}

.progress-item span:not(.check-icon) {
  color: #000000; /* Negro */
}

.progress-item:last-child {
  margin-bottom: 0;
}

.check-icon {
  color: #a855f7;
  font-size: 1.25rem;
}

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

  .features {
    padding: 60px 24px;
  }

  .features-title {
    font-size: 2rem;
  }

  .features-subtitle {
    font-size: 1.125rem;
    margin-bottom: 48px;
  }

  .features-grid {
    gap: 24px;
  }

  .how-it-works {
    padding: 60px 24px;
  }

  .how-it-works-title {
    font-size: 2.5rem;
  }

  .step-card {
    flex-direction: column;
    padding: 24px;
  }

  .step-number {
    width: 40px;
    height: 40px;
    font-size: 1.25rem;
  }

  .interaction-layout {
    flex-direction: column;
    gap: 24px;
  }

  .interaction-info,
  .chat-demo {
    min-width: 100%;
  }

  .tracking-layout {
    flex-direction: column;
    gap: 24px;
  }

  .tracking-info,
  .progress-items {
    min-width: 100%;
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

  .features {
    padding: 40px 16px;
  }

  .features-title {
    font-size: 1.75rem;
  }

  .features-subtitle {
    font-size: 1rem;
    margin-bottom: 32px;
  }

  .how-it-works {
    padding: 40px 16px;
  }

  .how-it-works-title {
    font-size: 2rem;
  }

  .how-it-works-subtitle {
    font-size: 1rem;
  }

  .step-content h3 {
    font-size: 1.25rem;
  }
}

/* Testimonials Section */
.testimonials {
  padding: 80px 24px;
  background: #f8fafc;
}

.testimonials-container {
  max-width: 1200px;
  margin: 0 auto;
}

.testimonials-title {
  font-size: 2.5rem;
  font-weight: 700;
  text-align: center;
  color: #1a1a1a;
  margin-bottom: 64px;
}

.testimonials-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 32px;
}

.testimonial-card {
  background: white;
  padding: 32px;
  border-radius: 24px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease;
}

.testimonial-card:hover {
  transform: translateY(-4px);
}

.testimonial-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 1.25rem;
}

.user-info h4 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.user-info span {
  font-size: 0.875rem;
  color: #64748b;
}

.testimonial-text {
  color: #4a5568;
  line-height: 1.6;
  font-style: italic;
}

@media (max-width: 768px) {
  .testimonials {
    padding: 60px 24px;
  }

  .testimonials-title {
    font-size: 2rem;
    margin-bottom: 48px;
  }

  .testimonials-grid {
    gap: 24px;
  }
}

@media (max-width: 480px) {
  .testimonials {
    padding: 40px 16px;
  }

  .testimonials-title {
    font-size: 1.75rem;
    margin-bottom: 32px;
  }

  .testimonial-card {
    padding: 24px;
  }
}

/* Final CTA Section */
.final-cta {
  padding: 120px 24px;
  background: white;
  text-align: center;
}

.final-cta-container {
  max-width: 800px;
  margin: 0 auto;
}

.final-cta-title {
  font-size: 3rem;
  font-weight: 800;
  color: #1a1a1a;
  margin-bottom: 24px;
}

.final-cta-subtitle {
  font-size: 1.25rem;
  color: #4a5568;
  line-height: 1.7;
  margin-bottom: 48px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.final-cta-button {
  background: linear-gradient(135deg, #a855f7 0%, #8b5cf6 100%);
  border: none;
  padding: 16px 32px;
  font-size: 16px;
  font-weight: 600;
  height: auto;
  box-shadow: 0 4px 14px rgba(168, 85, 247, 0.4);
  transition: all 0.3s ease;
}

.final-cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(168, 85, 247, 0.5);
}

@media (max-width: 768px) {
  .final-cta {
    padding: 80px 24px;
  }

  .final-cta-title {
    font-size: 2.5rem;
  }

  .final-cta-subtitle {
    font-size: 1.125rem;
  }
}

@media (max-width: 480px) {
  .final-cta {
    padding: 60px 16px;
  }

  .final-cta-title {
    font-size: 2rem;
  }

  .final-cta-subtitle {
    font-size: 1rem;
  }
}
</style>