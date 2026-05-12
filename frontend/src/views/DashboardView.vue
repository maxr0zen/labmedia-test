<template>
  <div class="dashboard">
    <h1>Дашборд</h1>
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-value">{{ stats.clients }}</div>
        <div class="stat-label">Клиентов</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ stats.payments }}</div>
        <div class="stat-label">Платежей</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ formatMoney(stats.total) }}</div>
        <div class="stat-label">Общий объём</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ formatMoney(stats.avg) }}</div>
        <div class="stat-label">Средний платёж</div>
      </div>
    </div>
    <DashboardCharts :clients="clientsStore.clients" :payments="paymentsStore.payments" />
    <div class="recent-section">
      <h2>Последние платежи</h2>
      <PaymentsTable
        :payments="paymentsStore.payments.slice(0, 10)"
        :pagination="{ count: 10, pageSize: 10, page: 1, next: null, previous: null }"
        :local-mode="true"
        @fetch="() => {}"
        @create="openModal()"
      />
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <h2>Новый платёж</h2>
        <PaymentForm
          :payment="selectedPayment"
          :clients="clientsStore.clients"
          :loading="paymentsStore.loading"
          @submit="handleSubmit"
          @cancel="closeModal"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useClientsStore } from '../store/clients'
import { usePaymentsStore } from '../store/payments'
import DashboardCharts from '../components/DashboardCharts.vue'
import PaymentsTable from '../components/PaymentsTable.vue'
import PaymentForm from '../components/PaymentForm.vue'

const clientsStore = useClientsStore()
const paymentsStore = usePaymentsStore()
const showModal = ref(false)
const selectedPayment = ref(null)
const isEdit = ref(false)

const stats = computed(() => {
  const payments = paymentsStore.payments
  const total = payments.reduce((sum, p) => sum + Number(p.amount), 0)
  return {
    clients: clientsStore.pagination.count || clientsStore.clients.length,
    payments: paymentsStore.pagination.count || payments.length,
    total,
    avg: payments.length ? total / payments.length : 0,
  }
})

onMounted(() => {
  clientsStore.fetchClients({ page_size: 1000 })
  paymentsStore.fetchPayments({ page_size: 100 })
})

function openModal(payment = null) {
  selectedPayment.value = payment
  isEdit.value = !!payment
  showModal.value = true
}

function closeModal() {
  showModal.value = false
  selectedPayment.value = null
}

async function handleSubmit(data) {
  try {
    if (isEdit.value) {
      await paymentsStore.updatePayment(selectedPayment.value.id, data)
    } else {
      await paymentsStore.createPayment(data)
    }
    closeModal()
  } catch (e) {}
}

function formatMoney(val) {
  return '$' + Number(val).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

h1 {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1a237e;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  text-align: center;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1a237e;
}

.stat-label {
  font-size: 0.9rem;
  color: #777;
  margin-top: 4px;
}

.recent-section h2 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 12px;
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
  font-size: 1.25rem;
}
</style>
