<template>
  <form class="form" @submit.prevent="handleSubmit">
    <div class="form-group">
      <label>Payer</label>
      <select v-model="form.payer" required>
        <option disabled value="">Select client</option>
        <option v-for="c in clients" :key="c.id" :value="c.id">
          {{ c.first_name }} {{ c.last_name }} ({{ c.country }})
        </option>
      </select>
    </div>
    <div class="form-group">
      <label>Amount</label>
      <input v-model="form.amount" type="number" step="0.01" min="0.01" required />
    </div>
    <div class="form-group">
      <label>Percent</label>
      <input v-model="form.percent" type="number" min="0" max="100" required />
    </div>
    <div class="form-group">
      <label>Pay Date</label>
      <input v-model="form.pay_date" type="datetime-local" required />
    </div>
    <div class="form-actions">
      <button type="submit" class="btn btn-primary" :disabled="loading">
        {{ isEdit ? 'Update' : 'Create' }}
      </button>
      <button type="button" class="btn btn-secondary" @click="$emit('cancel')">Cancel</button>
    </div>
  </form>
</template>

<script setup>
import { reactive, watch, computed } from 'vue'

const props = defineProps({
  payment: { type: Object, default: null },
  clients: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
})

const emit = defineEmits(['submit', 'cancel'])

const isEdit = computed(() => !!props.payment)

const form = reactive({
  payer: '',
  amount: '',
  percent: '',
  pay_date: '',
})

function formatDateTimeLocal(date) {
  if (!date) return ''
  const d = new Date(date)
  d.setMinutes(d.getMinutes() - d.getTimezoneOffset())
  return d.toISOString().slice(0, 16)
}

watch(() => props.payment, (val) => {
  if (val) {
    form.payer = val.payer || ''
    form.amount = val.amount || ''
    form.percent = val.percent || ''
    form.pay_date = formatDateTimeLocal(val.pay_date)
  }
}, { immediate: true })

function handleSubmit() {
  const payload = {
    payer: Number(form.payer),
    amount: form.amount,
    percent: Number(form.percent),
    pay_date: new Date(form.pay_date).toISOString(),
  }
  emit('submit', payload)
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

.form-group input,
.form-group select {
  padding: 10px 14px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.2s;
  background: white;
}

.form-group input:focus,
.form-group select:focus {
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
