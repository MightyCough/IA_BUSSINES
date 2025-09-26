<template>
  <div class="login-page">
    <!-- Lado izquierdo: Contenido hero -->
    <div class="hero-side">
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

        <!-- Cards de proceso -->
        <div class="process-cards">
          <div class="process-card">
            <div class="process-icon">🚀</div>
            <div class="process-content">
              <h3>Acelera tu crecimiento</h3>
              <p>Estrategias personalizadas para cada etapa</p>
            </div>
          </div>
          <div class="process-card">
            <div class="process-icon">💡</div>
            <div class="process-content">
              <h3>Ideas validadas por IA</h3>
              <p>Análisis de mercado en tiempo real</p>
            </div>
          </div>
          <div class="process-card">
            <div class="process-icon">📊</div>
            <div class="process-content">
              <h3>Análisis de mercado instantáneo</h3>
              <p>Datos y tendencias actualizadas</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Lado derecho: Formulario de login -->
    <div class="login-side">
      <div class="login-container">
        <!-- Header -->
        <div class="login-header">
          <div class="logo">
            <span class="logo-text">StarNow</span>
          </div>
          
          <button class="close-button" @click="goBack">
            <n-icon size="24">
              <CloseOutline />
            </n-icon>
          </button>
        </div>

        <!-- Formulario -->
        <div class="login-form-container">
          <h2 class="login-title">Iniciar sesión</h2>
          <p class="login-subtitle">Accede a tu asesor de negocios inteligente</p>

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
              />
            </n-form-item>

            <n-form-item>
              <n-button
                type="primary"
                size="large"
                block
                class="login-button"
                @click="handleLogin"
                :loading="authStore.isLoading"
                :disabled="authStore.isLoading"
              >
                {{ authStore.isLoading ? 'Iniciando sesión...' : 'Acceder' }}
              </n-button>
            </n-form-item>

            <!-- Separador -->
            <div class="separator">
              <div class="separator-line"></div>
              <span class="separator-text">O continúa con</span>
              <div class="separator-line"></div>
            </div>

            <!-- Botones OAuth -->
            <div class="oauth-buttons">
              <n-button
                size="large"
                class="oauth-button"
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
                class="oauth-button"
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

            <!-- Mostrar errores del store -->
            <n-form-item v-if="authStore.error">
              <n-alert 
                title="Error" 
                type="error" 
                :description="authStore.error"
                show-icon
                closable
                @close="authStore.clearError"
              />
            </n-form-item>
          </n-form>

          <!-- Footer del formulario -->
          <div class="login-footer">
            <p>¿No tienes una cuenta? 
              <router-link to="/register" class="register-link">
                Regístrate gratis
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
import { useMessage } from 'naive-ui'
import { useAuthStore } from '../stores/auth'
import { LogoGoogle, CloseOutline } from '@vicons/ionicons5'
import { h } from 'vue'

const authStore = useAuthStore()
const message = useMessage()
const router = useRouter()

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

// Reactive data
const email = ref('')
const password = ref('')

// Métodos
const handleLogin = async () => {
  authStore.clearError()
  
  if (!email.value || !password.value) {
    message.error('Todos los campos son requeridos')
    return
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(email.value)) {
    message.error('Por favor ingresa un email válido')
    return
  }
  
  try {
    await authStore.login({
      email: email.value,
      password: password.value
    })
    
    message.success('¡Bienvenido de vuelta!')
    router.push('/interfaz')
    
  } catch (error) {
    console.error('Error en login:', error)
    
    if (error.detail && error.detail.includes('incorrectos')) {
      message.error('Email o contraseña incorrectos')
    } else if (error.detail) {
      message.error(error.detail)
    } else {
      message.error('Error al iniciar sesión. Inténtalo de nuevo.')
    }
  }
}

const handleGoogleLogin = () => {
  message.info('Próximamente disponible')
}

const handleMicrosoftLogin = () => {
  message.info('Próximamente disponible')
}

const goBack = () => {
  router.push('/')
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 1fr 1fr;
  background: white;
}

/* Lado izquierdo: Hero */
.hero-side {
  background: linear-gradient(135deg, #a855f7 0%, #8b5cf6 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px 40px;
  color: white;
}

.hero-container {
  max-width: 500px;
  text-align: center;
}

.hero-badge {
  display: inline-block;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  padding: 8px 20px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 32px;
  backdrop-filter: blur(10px);
}

.hero-title {
  font-size: 3rem;
  font-weight: 700;
  line-height: 1.1;
  margin: 0 0 24px 0;
  letter-spacing: -0.02em;
}

.highlight {
  color: #fbbf24;
}

.hero-subtitle {
  font-size: 1.125rem;
  line-height: 1.7;
  opacity: 0.9;
  margin: 0 0 60px 0;
  font-weight: 400;
}

.process-cards {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.process-card {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  padding: 20px;
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  gap: 16px;
  text-align: left;
}

.process-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.process-content h3 {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0 0 4px 0;
}

.process-content p {
  font-size: 0.9rem;
  opacity: 0.8;
  margin: 0;
}

/* Lado derecho: Login */
.login-side {
  display: flex;
  flex-direction: column;
  background: white;
}

.login-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 40px;
}

.login-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 60px;
}

.logo-text {
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #a855f7 0%, #8b5cf6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.close-button {
  background: none;
  border: none;
  padding: 8px;
  border-radius: 50%;
  color: #666;
  cursor: pointer;
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
  max-width: 400px;
  margin: 0 auto;
  width: 100%;
}

.login-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 8px 0;
  text-align: center;
}

.login-subtitle {
  color: #666;
  text-align: center;
  margin: 0 0 40px 0;
  font-size: 1rem;
}

.login-form {
  margin-bottom: 32px;
}

.login-input {
  --n-border: 1px solid #e2e8f0;
  --n-border-focus: 1px solid #a855f7;
  --n-border-hover: 1px solid #a855f7;
  margin-bottom: 16px;
}

.login-button {
  background: linear-gradient(135deg, #a855f7 0%, #8b5cf6 100%);
  border: none;
  font-weight: 600;
  height: 48px;
  font-size: 1rem;
}

.separator {
  display: flex;
  align-items: center;
  margin: 32px 0;
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

.oauth-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 32px;
}

.oauth-button {
  background: white;
  border: 1px solid #e2e8f0;
  color: #374151;
  font-weight: 500;
  height: 48px;
  transition: all 0.2s;
}

.oauth-button:hover {
  border-color: #a855f7;
  background: rgba(168, 85, 247, 0.05);
}

.login-footer {
  text-align: center;
  margin-top: auto;
  padding-top: 32px;
  border-top: 1px solid #e2e8f0;
}

.login-footer p {
  color: #666;
  margin: 0;
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
  .login-page {
    grid-template-columns: 1fr;
  }
  
  .hero-side {
    display: none;
  }
  
  .login-container {
    padding: 40px 24px;
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  
  .login-container {
    padding: 32px 20px;
  }
  
  .login-title {
    font-size: 1.75rem;
  }
  
  .oauth-buttons {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .login-header {
    margin-bottom: 40px;
  }
}
</style>