<template>
  <div class="toast-container">
    <transition-group name="toast">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        class="toast"
        :class="toast.type"
      >
        {{ toast.message }}
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { addWebSocketListener } from '../websocket'

const toasts = ref([])
let idCounter = 0

function addToast(message, type = 'info') {
  const id = ++idCounter
  toasts.value.push({ id, message, type })
  setTimeout(() => {
    toasts.value = toasts.value.filter((t) => t.id !== id)
  }, 4000)
}

onMounted(() => {
  addWebSocketListener((data) => {
    if (data.type === 'model_update') {
      const model = data.model === 'client' ? 'Клиент' : 'Платёж'
      const actionMap = {
        create: 'создан',
        update: 'обновлён',
        delete: 'удалён',
      }
      const action = actionMap[data.action] || data.action
      addToast(`${model} #${data.id} ${action}`, 'success')
    }
  })
})
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 72px;
  right: 24px;
  z-index: 200;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.toast {
  padding: 12px 20px;
  border-radius: 8px;
  color: white;
  font-weight: 500;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  min-width: 200px;
}

.toast.success { background: #4caf50; }
.toast.info { background: #2196f3; }
.toast.warning { background: #ff9800; }
.toast.error { background: #f44336; }

.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%);
}
</style>
