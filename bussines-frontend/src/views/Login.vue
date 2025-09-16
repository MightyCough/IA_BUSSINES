<template>
  <div class="login-page">
    <!-- Video de fondo -->
    <div class="video-section">
      <!-- Opción 1: Video local -->
      <video 
        class="background-video"
        autoplay 
        muted 
        loop
        playsinline
      >
        <source src="/videos/business-hero.mp4" type="video/mp4">
        <source src="/videos/business-hero.webm" type="video/webm">
        Tu navegador no soporta videos HTML5.
      </video>
      
      <!-- Overlay para mejor legibilidad -->
      <div class="video-overlay"></div>
      
      <!-- Contenido sobre el video -->
      <div class="video-content">
        <div class="hero-badge">
          IA especializada para emprendedores
        </div>
        
        <h1 class="hero-title">
          Tu asesor de<br>
          Negocios <span class="highlight">inteligente</span>
        </h1>
        
        <p class="hero-subtitle">
          Desde la idea hasta la expansión. Recibe asesoría personalizada, 
          planes de negocio guiados y estrategias de crecimiento adaptadas a tu emprendimiento.
        </p>
        
        <!-- Características destacadas -->
        <div class="features-list">
          <div class="feature-item">
            <div class="feature-icon">🚀</div>
            <span>Acelera tu crecimiento</span>
          </div>
          <div class="feature-item">
            <div class="feature-icon">💡</div>
            <span>Ideas validadas por IA</span>
          </div>
          <div class="feature-item">
            <div class="feature-icon">📊</div>
            <span>Análisis de mercado instantáneo</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Panel lateral de login -->
    <div class="login-panel">
      <div class="login-container">
        <!-- Header del panel -->
        <div class="panel-header">
          <div class="logo">StarNow</div>
          <button class="close-button" @click="goBack">
            <n-icon size="24">
              <CloseOutline />
            </n-icon>
          </button>
        </div>

        <!-- Formulario de login -->
        <div class="login-form-container">
          <div class="login-header">
            <h2 class="login-title">Iniciar sesión</h2>
            <p class="login-subtitle">Accede a tu asesor de negocios inteligente</p>
          </div>

          <n-form class="login-form">
            <n-form-item>
              <n-input
                v-model:value="email"
                size="large"
                placeholder="Correo electrónico"
                class="login-input"
                type="email"
              />
            </n-form-item>

            <n-form-item>
              <n-input
                v-model:value="password"
                size="large"
                type="password"
                placeholder="Contraseña"
                class="login-input"
                show-password-on="click"
                @keyup.enter="handleLogin"
              />
            </n-form-item>

            <n-form-item>
              <n-button
                type="primary"
                size="large"
                block
                class="login-button"
                @click="handleLogin"
                :loading="loading"
              >
                Acceder
              </n-button>
            </n-form-item>

            <!-- Separador -->
            <div class="separator">
              <div class="separator-line"></div>
              <span class="separator-text">O continúa con</span>
              <div class="separator-line"></div>
            </div>

            <!-- Botones de OAuth -->
            <div class="oauth-buttons">
              <n-button
                size="large"
                class="oauth-button google-button"
                @click="handleGoogleLogin"
              >
                <template #icon>
                  <n-icon size="20">
                    <LogoGoogle />
                  </n-icon>
                </template>
                Google
              </n-button>

              <n-button
                size="large"
                class="oauth-button microsoft-button"
                @click="handleMicrosoftLogin"
              >
                <template #icon>
                  <n-icon size="20">
                    <LogoMicrosoft />
                  </n-icon>
                </template>
                Microsoft
              </n-button>
            </div>
          </n-form>

          <!-- Enlace a registro -->
          <div class="login-footer">
            <p>¿No tienes cuenta? 
              <router-link to="/register" class="register-link">
                Crear cuenta gratuita
              </router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { LogoGoogle, CloseOutline } from '@vicons/ionicons5'
import { h } from 'vue'

// Icono de Microsoft
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
const email = ref('')
const password = ref('')
const loading = ref(false)

// Methods
const handleLogin = async () => {
  if (!email.value || !password.value) {
    console.error('Por favor completa todos los campos')
    return
  }

  loading.value = true
  
  try {
    console.log('Login attempt:', { email: email.value, password: password.value })
    
    // Simular login exitoso
    setTimeout(() => {
      loading.value = false
      router.push('/interfaz')
    }, 1500)
    
  } catch (error) {
    loading.value = false
    console.error('Error de login:', error)
  }
}

const handleGoogleLogin = () => {
  console.log('Google login')
  // Redirigir a interfaz después del login exitoso
  router.push('/interfaz')
}

const handleMicrosoftLogin = () => {
  console.log('Microsoft login')
  // Redirigir a interfaz después del login exitoso
  router.push('/interfaz')
}

const goBack = () => {
  router.push('/')
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  background: #000;
}

/* Sección del video */
.video-section {
  flex: 1;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.background-video {
  position: absolute;
  top: 50%;
  left: 50%;
  min-width: 100%;
  min-height: 100%;
  width: auto;
  height: auto;
  transform: translate(-50%, -50%);
  object-fit: cover;
  z-index: 1;
}

.video-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    45deg, 
    rgba(168, 85, 247, 0.7) 0%, 
    rgba(139, 92, 246, 0.6) 50%,
    rgba(168, 85, 247, 0.8) 100%
  );
  z-index: 2;
}

.video-content {
  position: relative;
  z-index: 3;
  text-align: center;
  color: white;
  max-width: 600px;
  padding: 0 40px;
}

.hero-badge {
  display: inline-block;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  color: white;
  padding: 10px 24px;
  border-radius: 25px;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 32px;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  line-height: 1.1;
  margin: 0 0 24px 0;
  letter-spacing: -0.02em;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.highlight {
  background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: none;
}

.hero-subtitle {
  font-size: 1.2rem;
  line-height: 1.6;
  margin: 0 0 48px 0;
  opacity: 0.95;
  font-weight: 400;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.features-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-width: 400px;
  margin: 0 auto;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 16px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  padding: 16px 20px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  font-weight: 500;
}

.feature-icon {
  font-size: 24px;
  width: 40px;
  text-align: center;
}

/* Panel lateral de login */
.login-panel {
  width: 480px;
  background: white;
  display: flex;
  flex-direction: column;
  box-shadow: -10px 0 30px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 10;
}

.login-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 32px;
  border-bottom: 1px solid #f0f0f0;
}

.logo {
  font-size: 24px;
  font-weight: 700;
  color: #a855f7;
  letter-spacing: -0.01em;
}

.close-button {
  background: none;
  border: none;
  padding: 8px;
  border-radius: 8px;
  cursor: pointer;
  color: #666;
  transition: background 0.2s;
}

.close-button:hover {
  background: #f5f5f5;
}

.login-form-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 40px 32px;
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.login-title {
  font-size: 28px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 8px 0;
  letter-spacing: -0.01em;
}

.login-subtitle {
  color: #666;
  margin: 0;
  font-size: 15px;
}

.login-form {
  margin-bottom: 32px;
}

.login-input {
  --n-border-radius: 12px;
  --n-height: 56px;
  --n-font-size: 16px;
  --n-border: 1px solid #e2e8f0;
  --n-border-focus: 2px solid #a855f7;
  --n-border-hover: 1px solid #a855f7;
  margin-bottom: 16px;
}

.login-button {
  background: linear-gradient(135deg, #a855f7 0%, #8b5cf6 100%);
  border: none;
  height: 56px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 12px;
  box-shadow: 0 4px 14px rgba(168, 85, 247, 0.3);
  transition: all 0.3s ease;
  margin-bottom: 24px;
}

.login-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(168, 85, 247, 0.4);
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
  font-weight: 500;
}

.oauth-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 24px;
}

.oauth-button {
  background: white;
  border: 1px solid #e2e8f0;
  color: #374151;
  font-weight: 500;
  height: 48px;
  border-radius: 10px;
  transition: all 0.2s;
}

.oauth-button:hover {
  border-color: #d1d5db;
  background: #f9fafb;
  transform: translateY(-1px);
}

.google-button:hover {
  border-color: #4285f4;
  background: rgba(66, 133, 244, 0.05);
}

.microsoft-button:hover {
  border-color: #0078d4;
  background: rgba(0, 120, 212, 0.05);
}

.login-footer {
  text-align: center;
  margin-top: auto;
  padding-top: 24px;
  border-top: 1px solid #f0f0f0;
}

.login-footer p {
  color: #666;
  margin: 0;
  font-size: 14px;
}

.register-link {
  color: #a855f7;
  text-decoration: none;
  font-weight: 600;
}

.register-link:hover {
  text-decoration: underline;
}

/* Responsive */
@media (max-width: 1024px) {
  .login-panel {
    width: 420px;
  }
  
  .login-form-container {
    padding: 32px 24px;
  }
  
  .hero-title {
    font-size: 3rem;
  }
}

@media (max-width: 768px) {
  .login-page {
    flex-direction: column;
  }
  
  .video-section {
    height: 40vh;
    min-height: 300px;
  }
  
  .login-panel {
    width: 100%;
    height: 60vh;
  }
  
  .login-container {
    height: auto;
  }
  
  .video-content {
    padding: 0 24px;
  }
  
  .hero-title {
    font-size: 2.5rem;
  }
  
  .features-list {
    display: none;
  }
}

@media (max-width: 480px) {
  .panel-header {
    padding: 16px 20px;
  }
  
  .login-form-container {
    padding: 24px 20px;
  }
  
  .oauth-buttons {
    grid-template-columns: 1fr;
  }
  
  .hero-title {
    font-size: 2rem;
  }
}
</style>