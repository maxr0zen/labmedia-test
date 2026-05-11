<template>
  <div class="page">
    <div class="header">
      <button class="btn-back" @click="$router.back()">← Back</button>
      <h1>Payment #{{ id }}</h1>
    </div>
    <div v-if="paymentsStore.loading" class="loading">Loading...</div>
    <div v-else-if="paymentsStore.payment" class="detail-card">
      <div class="detail-grid">
        <div><strong>ID:</strong> {{ paymentsStore.payment.id }}</div>
        <div><strong>Payer:</strong>
          <router-link :to="`/clients/${paymentsStore.payment.payer}`" class="link">
            {{ paymentsStore.payment.payer_details?.first_name }} {{ paymentsStore.payment.payer_details?.last_name }}
          </router-link>
        </div>
        <div><strong>Amount:</strong> {{ formatMoney(paymentsStore.payment.amount) }}</div>
        <div><strong>Percent:</strong> {{ paymentsStore.payment.percent }}%</div>
        <div><strong>Date:</strong> {{ formatDate(paymentsStore.payment.pay_date) }}</div>
      </div>
      <div class="actions">
        <button class="btn btn-primary" @click="showEdit = true">Edit</button>
        <button class="btn btn-danger" @click="handleDelete">Delete</button>
      </div>
    </div>

    <div v-if="showEdit" class="modal-overlay" @click.self="showEdit = false">
      <div class="modal">
        <h2>Edit Payment</h2>
        <PaymentForm
          :payment="paymentsStore.payment"
          :clients="clientsStore.clients"
          :loading="paymentsStore.loading"
          @submit="handleUpdate"
          @cancel="showEdit = false"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePaymentsStore } from '../store/payments'
import { useClientsStore } from '../store/clients'
import PaymentForm from '../components/PaymentForm.vue'

const props = defineProps({ id: { type: String, required: true } })
const router = useRouter()
const paymentsStore = usePaymentsStore()
const clientsStore = useClientsStore()
const showEdit = ref(false)

onMounted(() => {
  paymentsStore.fetchPayment(props.id)
  clientsStore.fetchClients({ page_size: 1000 })
})

async function handleUpdate(data) {
  try {
    await paymentsStore.updatePayment(props.id, data)
    showEdit.value = false
  } catch (e) {}
}

async function handleDelete() {
  if (!confirm('Delete this payment?')) return
  try {
    await paymentsStore.deletePayment(props.id)
    router.push('/payments')
  } catch (e) {}
}

function formatMoney(val) {
  if (!val) return '$0.00'
  return '$' + Number(val).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

function formatDate(date) {
  if (!date) return ''
  return new Date(date).toLocaleString()
}
</script>

<style scoped>
.page {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.header {
  display: flex;
  align-items: center;
  gap: 16px;
}

.btn-back {
  background: #e0e0e0;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}

h1 {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1a237e;
}

.loading {
  padding: 40px;
  text-align: center;
  color: #777;
}

.detail-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}

.detail-grid div {
  font-size: 1rem;
  color: #444;
}

.link {
  color: #1a237e;
  text-decoration: none;
  font-weight: 500;
}

.link:hover {
  text-decoration: underline;
}

.actions {
  display: flex;
  gap: 12px;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
}

.btn-primary {
  background: #1a237e;
  color: white;
}

.btn-danger {
  background: #c62828;
  color: white;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 150;
}

.modal {
  background: white;
  border-radius: 12px;
  padding: 24px;
  width: 100%;
  max-width: 520px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.2);
}

.modal h2 {
  margin-bottom: 16px;
}
</style>
