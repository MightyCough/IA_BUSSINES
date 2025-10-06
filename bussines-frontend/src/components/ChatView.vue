<template>
  <div class="chat-container">
    <!-- Historial de conversación -->
    <div class="chat-messages">
      <div 
        v-for="(msg, index) in conversation" 
        :key="index" 
        :class="['chat-message', msg.role]"
      >
        <div class="message-bubble">
          <strong v-if="msg.role === 'user'">Tú:</strong>
          <strong v-else>IA:</strong>
          <p>{{ msg.content }}</p>
        </div>
      </div>
    </div>

    <!-- Input de mensaje -->
    <div class="chat-input">
      <n-input
        v-model:value="userMessage"
        type="textarea"
        placeholder="Escribe tu mensaje..."
        @keyup.enter.exact.prevent="sendMessage"
        :disabled="loading"
      />
      <n-button 
        type="primary" 
        @click="sendMessage" 
        :loading="loading"
      >
        Enviar
      </n-button>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { chatService } from "../services/chatService"

const userMessage = ref("")
const conversation = ref([]) // historial de mensajes
const loading = ref(false)

const sendMessage = async () => {
  if (!userMessage.value.trim()) return

  // 👉 agregar mensaje del usuario
  conversation.value.push({
    role: "user",
    content: userMessage.value
  })

  const currentMessage = userMessage.value
  userMessage.value = ""
  loading.value = true

  try {
    const response = await chatService.sendMessage(
      currentMessage,
      conversation.value // historial actual
    )

    if (response.success) {
      conversation.value.push({
        role: "assistant",
        content: response.data.response
      })
    } else {
      conversation.value.push({
        role: "assistant",
        content: `⚠️ Error: ${response.error}`
      })
    }
  } catch (e) {
    console.error("❌ Error en chat:", e)
    conversation.value.push({
      role: "assistant",
      content: "⚠️ Error inesperado al contactar con la IA."
    })
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 80vh;
  max-width: 800px;
  margin: 0 auto;
  padding: 16px;
  border: 1px solid #eee;
  border-radius: 12px;
  background: #fff;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
  margin-bottom: 16px;
  background: #f9f9f9;
  border-radius: 8px;
}

.chat-message {
  margin-bottom: 12px;
  display: flex;
}

.chat-message.user {
  justify-content: flex-end;
}

.chat-message.assistant {
  justify-content: flex-start;
}

.message-bubble {
  max-width: 70%;
  padding: 10px 14px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.4;
}

.chat-message.user .message-bubble {
  background: #a855f7;
  color: white;
  border-bottom-right-radius: 4px;
}

.chat-message.assistant .message-bubble {
  background: #e6e6e6;
  color: #333;
  border-bottom-left-radius: 4px;
}

.chat-input {
  display: flex;
  gap: 8px;
}
</style>
