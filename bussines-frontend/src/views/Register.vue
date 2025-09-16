<template>
  <div class="register-page">
    <!-- Contenido de fondo (blur) -->
    <div class="background-content">
      <div class="hero-container">
        <div class="hero-badge">
          IA especializada para emprendedores
        </div>

        <h1 class="hero-title">
          Tu asesor de<br>
          Negocios <span class="highlight">inteligente</span>
        </h1>

        <p class="hero-subtitle">
          Desde la idea hasta la expansión. Recibe asesoría personalizada, planes de negocio 
          guiados y estrategias de crecimiento adaptadas a tu emprendimiento.
        </p>

        <!-- Cards de proceso (ahora clickeables) -->
        <div class="process-cards">
          <div 
            class="process-card clickable-card" 
            @click="redirectToAuth"
          >
            <div class="process-content">
              <h3>Ya tienes tu idea</h3>
              <p>Valida y desarrolla tu concepto</p>
              <div class="card-overlay">
                <span class="card-cta">¡Comienza ahora!</span>
              </div>
            </div>
          </div>
          <div 
            class="process-card clickable-card" 
            @click="redirectToAuth"
          >
            <div class="process-content">
              <h3>Consolidar tu idea</h3>
              <p>Estructura y escala tu proyecto</p>
              <div class="card-overlay">
                <span class="card-cta">¡Comienza ahora!</span>
              </div>
            </div>
          </div>
          <div 
            class="process-card clickable-card" 
            @click="redirectToAuth"
          >
            <div class="process-content">
              <h3>Empezar de cero</h3>
              <p>Genera ideas y encuentra oportunidades</p>
              <div class="card-overlay">
                <span class="card-cta">¡Comienza ahora!</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Overlay blur -->
    <div class="overlay"></div>

    <!-- Modal de registro -->
    <div class="register-modal">
      <n-card class="register-card">
        <div class="register-header">
          <!-- ✅ CORREGIDO: Título correcto -->
          <h2 class="register-title">Registrarse</h2>
        </div>

        <n-form class="register-form">
          <n-form-item>
            <n-input
              v-model:value="name"
              size="large"
              placeholder="Nombre"
              class="register-input"
            />
          </n-form-item>

          <n-form-item>
            <n-input
              v-model:value="email"
              size="large"
              placeholder="Usuario"
              class="register-input"
            />
          </n-form-item>

          <n-form-item>
            <n-input
              v-model:value="password"
              size="large"
              type="password"
              placeholder="Contraseña"
              class="register-input"
              show-password-on="click"
            />
          </n-form-item>

          <n-form-item>
            <n-button
              type="primary"
              size="large"
              block
              class="register-button"
              @click="handleRegister"
            >
              <!-- ✅ CORREGIDO: Texto correcto -->
              Registrarse
            </n-button>
          </n-form-item>

          <!-- Separador -->
          <div class="separator">
            <div class="separator-line"></div>
            <span class="separator-text">O</span>
            <div class="separator-line"></div>
          </div>

          <!-- Botones de OAuth -->
          <n-form-item>
            <n-button
              size="large"
              block
              class="oauth-button google-button"
              @click="handleGoogleRegister"
            >
              <template #icon>
                <n-icon size="20">
                  <LogoGoogle />
                </n-icon>
              </template>
              Continuar con Google
            </n-button>
          </n-form-item>

          <n-form-item>
            <n-button
              size="large"
              block
              class="oauth-button microsoft-button"
              @click="handleMicrosoftRegister"
            >
              <template #icon>
                <n-icon size="20">
                  <LogoMicrosoft />
                </n-icon>
              </template>
              Continuar con Microsoft
            </n-button>
          </n-form-item>
        </n-form>

        <!-- Enlace a login -->
        <div class="register-footer">
          <!-- ✅ CORREGIDO: Texto correcto -->
          <p>¿Ya tienes cuenta? 
            <router-link to="/login" class="login-link">
              Inicia sesión aquí
            </router-link>
          </p>
        </div>

        <!-- Botón cerrar -->
        <n-button
          text
          class="close-button"
          @click="goBack"
        >
          <n-icon size="24">
            <CloseOutline />
          </n-icon>
        </n-button>
      </n-card>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { LogoGoogle, CloseOutline } from '@vicons/ionicons5'
import { h } from 'vue'

// Icono de Microsoft (creamos uno simple)
const LogoMicrosoft = {
  render() {
    return h('svg', {
      viewBox: '0 0 24 24',
      fill: 'currentColor'
    }, [
      h('path', {
        d: 'M11.4 24H0V12.6h11.4V24zM24 24H12.6V12.6H24V24zM11.4 11.4H0V0h11.4v11.4zM24 11.4H12.6V0H24v11.4z'
      })
    ])
  }
}

const router = useRouter()

// Reactive data
const name = ref('')
const email = ref('')
const password = ref('')

// Methods
const handleRegister = () => {
  if (!name.value || !email.value || !password.value) {
    console.error('Todos los campos son requeridos')
    return
  }
  
  if (password.value.length < 6) {
    console.error('La contraseña debe tener al menos 6 caracteres')
    return
  }
  
  console.log('Register attempt:', { 
    name: name.value, 
    email: email.value, 
    password: password.value 
  })
  // Aquí irá la lógica de registro
}

const handleGoogleRegister = () => {
  console.log('Google register')
  // Aquí irá la lógica de Google OAuth
}

const handleMicrosoftRegister = () => {
  console.log('Microsoft register')
  // Aquí irá la lógica de Microsoft OAuth
}

// ✅ NUEVO: Función para redirigir al hacer click en las cards
const redirectToAuth = () => {
  // Puedes cambiarlo a '/login' si prefieres que vaya al login
  router.push('/register')
}

const goBack = () => {
  router.push('/')
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Contenido de fondo */
.background-content {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
  padding: 60px 24px;
  text-align: center;
}

.hero-container {
  max-width: 1200px;
  margin: 0 auto;
  padding-top: 80px;
}

.hero-badge {
  display: inline-block;
  background: linear-gradient(135deg, #a855f7 0%, #8b5cf6 100%);
  color: white;
  padding: 8px 20px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 32px;
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
  max-width: 1000px;
  margin: 0 auto;
}

.process-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 32px 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
}

/* ✅ NUEVO: Estilos para cards clickeables */
.clickable-card {
  cursor: pointer;
  transition: all 0.3s ease;
}

.clickable-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(168, 85, 247, 0.2);
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
  font-size: 1.1rem;
  font-weight: 600;
  text-align: center;
  transform: translateY(10px);
  transition: transform 0.3s ease;
}

.clickable-card:hover .card-cta {
  transform: translateY(0);
}

.process-content h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 12px 0;
}

.process-content p {
  font-size: 0.95rem;
  color: #64748b;
  margin: 0;
}

/* Overlay blur */
.overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(8px);
  z-index: 1;
}

/* Modal de registro */
.register-modal {
  position: relative;
  z-index: 2;
  width: 100%;
  max-width: 420px;
  margin: 0 16px;
}

.register-card {
  position: relative;
  padding: 40px;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  background: white;
}

.close-button {
  position: absolute;
  top: 16px;
  right: 16px;
  padding: 8px;
  border-radius: 50%;
  color: #666;
}

.close-button:hover {
  background: #f5f5f5;
}

.register-header {
  text-align: center;
  margin-bottom: 32px;
}

.register-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.register-form {
  margin-bottom: 24px;
}

.register-input {
  --n-border: 1px solid #e2e8f0;
  --n-border-focus: 1px solid #a855f7;
  --n-border-hover: 1px solid #a855f7;
}

.register-button {
  background: linear-gradient(135deg, #a855f7 0%, #8b5cf6 100%);
  border: none;
  font-weight: 600;
  margin-bottom: 24px;
}

.separator {
  display: flex;
  align-items: center;
  margin: 24px 0;
}

.separator-line {
  flex: 1;
  height: 1px;
  background: #e2e8f0;
}

.separator-text {
  margin: 0 16px;
  color: #666;
  font-size: 14px;
}

.oauth-button {
  background: white;
  border: 1px solid #e2e8f0;
  color: #374151;
  font-weight: 500;
  margin-bottom: 12px;
  transition: all 0.2s;
}

.oauth-button:hover {
  border-color: #d1d5db;
  background: #f9fafb;
}

.google-button:hover {
  border-color: #4285f4;
  background: rgba(66, 133, 244, 0.05);
}

.microsoft-button:hover {
  border-color: #0078d4;
  background: rgba(0, 120, 212, 0.05);
}

.register-footer {
  text-align: center;
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #e2e8f0;
}

.register-footer p {
  color: #666;
  margin: 0;
}

.login-link {
  color: #a855f7;
  text-decoration: none;
  font-weight: 600;
}

.login-link:hover {
  text-decoration: underline;
}

/* Responsive */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  
  .register-card {
    padding: 32px 24px;
    margin: 0 16px;
  }
  
  .process-cards {
    grid-template-columns: 1fr;
    gap: 16px;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .register-card {
    padding: 24px 20px;
  }
}
</style>