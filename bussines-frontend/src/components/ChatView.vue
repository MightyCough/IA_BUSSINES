<template>
    <div class="chat-view">
      <div class="chat-header">
        <h1>Historial de chats</h1>
        <n-button type="primary" @click="newChat">
          + Nueva conversación
        </n-button>
      </div>
  
      <div class="chat-search">
        <n-input
          v-model:value="searchQuery"
          placeholder="Buscar en chats..."
          clearable
        >
          <template #prefix>
            <n-icon><SearchOutline /></n-icon>
          </template>
        </n-input>
      </div>
  
      <div class="chat-list">
        <div class="chat-stats">
          <span>{{ chatCount }} chats con StarNow</span>
          <n-button text type="primary">Seleccionar</n-button>
        </div>
  
        <div class="chat-items">
          <div 
            v-for="chat in filteredChats" 
            :key="chat.id" 
            class="chat-item"
            @click="openChat(chat.id)"
          >
            <div class="chat-item-content">
              <div class="chat-title">{{ chat.title }}</div>
              <div class="chat-preview">{{ chat.preview }}</div>
            </div>
            <div class="chat-meta">
              <span class="chat-date">{{ chat.date }}</span>
              <n-button circle text type="primary">
                <template #icon>
                  <n-icon><EllipsisHorizontal /></n-icon>
                </template>
              </n-button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue'
  import { SearchOutline, EllipsisHorizontal } from '@vicons/ionicons5'
  import { useRouter } from 'vue-router'
  
  const router = useRouter()
  const searchQuery = ref('')
  
  // Datos de ejemplo
  const chats = ref([
    {
      id: 1,
      title: 'Plan de negocio para startup',
      preview: 'Análisis de mercado y estrategias de crecimiento...',
      date: 'Hace 2 días'
    },
    {
      id: 2,
      title: 'Estrategia de marketing digital',
      preview: 'Desarrollo de campaña en redes sociales...',
      date: 'Hace 3 días'
    },
    {
      id: 3,
      title: 'Análisis financiero',
      preview: 'Proyecciones financieras y flujo de caja...',
      date: 'Hace 1 semana'
    }
  ])
  
  const chatCount = computed(() => chats.value.length)
  
  const filteredChats = computed(() => {
    const query = searchQuery.value.toLowerCase()
    return query
      ? chats.value.filter(chat => 
          chat.title.toLowerCase().includes(query) || 
          chat.preview.toLowerCase().includes(query)
        )
      : chats.value
  })
  
  const newChat = () => {
    router.push('/nueva-conversacion')
  }
  
  const openChat = (chatId) => {
    router.push(`/chat/${chatId}`)
  }
  </script>
  
  <style scoped>
  .chat-view {
    width: 100%;
    max-width: 800px;
    margin: 0 auto;
    padding: 24px;
  }
  
  .chat-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
  }
  
  .chat-header h1 {
    font-size: 24px;
    font-weight: 600;
    color: #333;
  }
  
  .chat-search {
    margin-bottom: 24px;
  }
  
  .chat-stats {
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #666;
    font-size: 14px;
    margin-bottom: 16px;
  }
  
  .chat-items {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  
  .chat-item {
    display: flex;
    justify-content: space-between;
    padding: 16px;
    border: 1px solid #eee;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .chat-item:hover {
    background-color: #f9f9f9;
    border-color: #ddd;
  }
  
  .chat-item-content {
    flex: 1;
  }
  
  .chat-title {
    font-size: 16px;
    font-weight: 500;
    color: #333;
    margin-bottom: 4px;
  }
  
  .chat-preview {
    font-size: 14px;
    color: #666;
  }
  
  .chat-meta {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  
  .chat-date {
    font-size: 13px;
    color: #666;
  }
  
  @media (max-width: 640px) {
    .chat-view {
      padding: 16px;
    }
  
    .chat-header h1 {
      font-size: 20px;
    }
  
    .chat-preview {
      display: none;
    }
  }
  </style>