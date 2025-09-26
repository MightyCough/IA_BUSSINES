<template>
  <div class="container proyecto-form-container">
    <h1 class="main-title">Crear un proyecto de emprendimiento</h1>
    <div class="proyecto-form-card">
      <div class="proyecto-form-group">
        <label for="nombreProyecto" class="proyecto-label">Nombre del emprendimiento</label>
        <n-input id="nombreProyecto" v-model:value="nombreProyecto" placeholder="Asigne un nombre a su proyecto" size="large" class="proyecto-input" />
      </div>
      <div class="proyecto-form-group">
        <label for="objetivoProyecto" class="proyecto-label">¿Qué está tratando de lograr?</label>
        <n-input id="objetivoProyecto" v-model:value="objetivoProyecto" type="textarea" placeholder="Describa su proyecto, objetivos, tema, etc." size="large" class="proyecto-textarea" :autosize="{ minRows: 3, maxRows: 6 }" />
      </div>
      <div class="proyecto-form-actions">
        <n-button type="primary" size="large" class="proyecto-submit" @click="crearProyecto" :disabled="!nombreProyecto.trim() || !objetivoProyecto.trim()">
          Crear proyecto
        </n-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useMessage } from 'naive-ui'

const nombreProyecto = ref("");
const objetivoProyecto = ref("");
const message = useMessage();

const crearProyecto = () => {
  if (!nombreProyecto.value.trim() || !objetivoProyecto.value.trim()) return;
  message.success("Proyecto creado exitosamente");
  // Aquí puedes agregar la lógica para guardar el proyecto
  nombreProyecto.value = "";
  objetivoProyecto.value = "";
};
</script>

<style scoped>
.proyecto-form-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 70vh;
}

.proyecto-form-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(168, 85, 247, 0.08), 0 1.5px 6px rgba(0,0,0,0.03);
  padding: 40px 32px;
  max-width: 480px;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 28px;
}

.proyecto-form-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.proyecto-label {
  font-size: 15px;
  font-weight: 600;
  color: #6b7280;
}

.proyecto-input,
.proyecto-textarea {
  --n-border-radius: 10px;
  --n-font-size: 16px;
  --n-border: 2px solid #e6e6e6;
  --n-border-focus: 2px solid #a855f7;
  --n-border-hover: 2px solid #a855f7;
  --n-padding-left: 18px;
  --n-padding-right: 18px;
}

.proyecto-textarea {
  min-height: 80px;
}

.proyecto-form-actions {
  display: flex;
  justify-content: flex-end;
}

.proyecto-submit {
  background: linear-gradient(135deg, #a855f7 0%, #8b5cf6 100%);
  border: none;
  font-weight: 600;
  font-size: 16px;
  box-shadow: 0 4px 14px rgba(168, 85, 247, 0.13);
  transition: all 0.3s ease;
}
.proyecto-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>