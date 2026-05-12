<template>
  <form class="form" @submit.prevent="handleSubmit">
    <div class="form-group">
      <label>Имя</label>
      <input v-model="form.first_name" type="text" required maxlength="100" />
    </div>
    <div class="form-group">
      <label>Фамилия</label>
      <input v-model="form.last_name" type="text" required maxlength="100" />
    </div>
    <div class="form-group">
      <label>Страна</label>
      <input v-model="form.country" type="text" required maxlength="100" />
    </div>
    <div class="form-actions">
      <button type="submit" class="btn btn-primary" :disabled="loading">
        {{ isEdit ? 'Обновить' : 'Создать' }}
      </button>
      <button type="button" class="btn btn-secondary" @click="$emit('cancel')">Отмена</button>
    </div>
  </form>
</template>

<script setup>
import { reactive, watch, computed } from 'vue'

const props = defineProps({
  client: { type: Object, default: null },
  loading: { type: Boolean, default: false },
})

const emit = defineEmits(['submit', 'cancel'])

const isEdit = computed(() => !!props.client)

const form = reactive({
  first_name: '',
  last_name: '',
  country: '',
})

watch(() => props.client, (val) => {
  if (val) {
    form.first_name = val.first_name || ''
    form.last_name = val.last_name || ''
    form.country = val.country || ''
  }
}, { immediate: true })

function handleSubmit() {
  emit('submit', { ...form })
}
</script>

<style scoped>
.form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #555;
}

.form-group input {
  padding: 10px 14px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: #1a237e;
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 8px;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: opacity 0.2s;
  font-weight: 600;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background: #1a237e;
  color: white;
}

.btn-secondary {
  background: #e0e0e0;
  color: #333;
}
</style>
