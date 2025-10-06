<template>
  <div class="verification-container">
    <div class="verification-card">
      <!-- Botón cerrar -->
      <button class="close-btn" @click="router.push('/login')">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
          <path d="M15 5L5 15M5 5L15 15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </button>

      <!-- Título -->
      <h1 class="title">Verificación de Email</h1>

      <!-- Ícono de correo -->
      <div class="email-icon">
        <svg width="64" height="64" viewBox="0 0 64 64" fill="none">
          <rect x="8" y="16" width="48" height="32" rx="4" stroke="#8B5CF6" stroke-width="2"/>
          <path d="M8 20L32 36L56 20" stroke="#8B5CF6" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </div>

      <!-- Mensaje -->
      <p class="message">
        Hemos enviado un código de verificación de 6 dígitos a tu correo:
      </p>
      <p class="email">{{ email }}</p>

      <!-- Formulario -->
      <form @submit.prevent="verifyCode" class="form">
        <div class="input-group">
          <input
            v-model="verificationCode"
            type="text"
            placeholder="Ingresa el código"
            maxlength="6"
            required
            class="input"
          />
        </div>

        <n-button
          type="primary"
          block
          size="large"
          attr-type="submit"
          class="submit-btn"
          :loading="isLoading"
        >
          Verificar Código
        </n-button>
      </form>

      <!-- Mensaje de error -->
      <n-alert v-if="errorMessage" type="error" class="error-alert">
        {{ errorMessage }}
      </n-alert>

      <!-- Separador -->
      <div class="divider">
        <span>O</span>
      </div>

      <!-- Reenviar código -->
      <div class="resend-section">
        <p class="resend-text">¿No recibiste el código?</p>
        <button 
          type="button" 
          class="resend-btn"
          @click="resendCode"
          :disabled="isResending"
        >
          {{ isResending ? 'Reenviando...' : 'Reenviar código' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRouter, useRoute } from "vue-router"
import { NButton, NAlert, useMessage } from "naive-ui"
import { authService } from "../services/authService"

const router = useRouter()
const route = useRoute()
const message = useMessage()

const email = ref("")
const verificationCode = ref("")
const errorMessage = ref("")
const isLoading = ref(false)
const isResending = ref(false)

const verifyCode = async () => {
  if (verificationCode.value.length !== 6) {
    errorMessage.value = "El código debe tener 6 dígitos"
    return
  }

  try {
    isLoading.value = true
    errorMessage.value = ""
    
    const res = await authService.verifyEmail(verificationCode.value)

    console.log('✅ Verificación OK. Token en LS:', localStorage.getItem('token'))
    console.log('👤 User en LS:', localStorage.getItem('user'))

    message.success('¡Email verificado exitosamente!')
    
    setTimeout(() => {
      router.replace('/interfaz')
    }, 500)
  } catch (error) {
    console.error("❌ Error al verificar el código:", error)
    errorMessage.value = error.detail || "Código inválido o expirado. Por favor, intenta nuevamente."
  } finally {
    isLoading.value = false
  }
}

const resendCode = async () => {
  try {
    isResending.value = true
    errorMessage.value = ""
    
    // Aquí debes implementar tu servicio de reenvío
    // await authService.resendVerificationCode(email.value)
    
    message.success('Código reenviado exitosamente')
  } catch (error) {
    console.error("❌ Error al reenviar el código:", error)
    errorMessage.value = "No se pudo reenviar el código. Intenta más tarde."
  } finally {
    isResending.value = false
  }
}

onMounted(() => {
  email.value = route.query.email || localStorage.getItem("pending_email") || ""
  
  if (!email.value) {
    message.warning('No se encontró el email. Redirigiendo...')
    router.push('/register')
  }
})
</script>

<style scoped>
.verification-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.verification-card {
  background: white;
  border-radius: 24px;
  padding: 40px 32px;
  max-width: 440px;
  width: 100%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  position: relative;
  animation: slideUp 0.4s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.close-btn {
  position: absolute;
  top: 20px;
  right: 20px;
  background: transparent;
  border: none;
  color: #9ca3af;
  cursor: pointer;
  padding: 8px;
  border-radius: 8px;
  transition: all 0.2s;
}

.close-btn:hover {
  background: #f3f4f6;
  color: #374151;
}

.title {
  font-size: 28px;
  font-weight: 700;
  color: #111827;
  text-align: center;
  margin: 0 0 32px 0;
}

.email-icon {
  display: flex;
  justify-content: center;
  margin-bottom: 24px;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.message {
  text-align: center;
  color: #6b7280;
  font-size: 15px;
  line-height: 1.6;
  margin: 0 0 8px 0;
}

.email {
  text-align: center;
  color: #8B5CF6;
  font-weight: 600;
  font-size: 16px;
  margin: 0 0 32px 0;
  word-break: break-word;
}

.form {
  margin-bottom: 24px;
}

.input-group {
  margin-bottom: 20px;
}

.input {
  width: 100%;
  padding: 14px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 16px;
  transition: all 0.3s;
  box-sizing: border-box;
  text-align: center;
  letter-spacing: 4px;
  font-weight: 600;
  font-size: 20px;
}

.input:focus {
  outline: none;
  border-color: #8B5CF6;
  box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.1);
}

.input::placeholder {
  letter-spacing: normal;
  font-size: 15px;
  font-weight: 400;
}

.submit-btn {
  background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
  border: none;
  border-radius: 12px;
  font-weight: 600;
  font-size: 16px;
  height: 48px;
  margin-top: 8px;
  transition: all 0.3s;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(139, 92, 246, 0.4);
}

.error-alert {
  margin-bottom: 20px;
  border-radius: 12px;
}

.divider {
  display: flex;
  align-items: center;
  text-align: center;
  margin: 32px 0;
  color: #9ca3af;
  font-size: 14px;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  border-bottom: 1px solid #e5e7eb;
}

.divider span {
  padding: 0 16px;
}

.resend-section {
  text-align: center;
}

.resend-text {
  color: #6b7280;
  font-size: 14px;
  margin: 0 0 12px 0;
}

.resend-btn {
  background: transparent;
  border: none;
  color: #8B5CF6;
  font-weight: 600;
  font-size: 15px;
  cursor: pointer;
  padding: 8px 16px;
  border-radius: 8px;
  transition: all 0.2s;
}

.resend-btn:hover:not(:disabled) {
  background: #f3f0ff;
}

.resend-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 480px) {
  .verification-card {
    padding: 32px 24px;
  }

  .title {
    font-size: 24px;
  }
}
</style>