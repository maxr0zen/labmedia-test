<template>
  <div class="dashboard">
    <h1>Dashboard</h1>
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-value">{{ stats.clients }}</div>
        <div class="stat-label">Clients</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ stats.payments }}</div>
        <div class="stat-label">Payments</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ formatMoney(stats.total) }}</div>
        <div class="stat-label">Total Volume</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ formatMoney(stats.avg) }}</div>
        <div class="stat-label">Average Payment</div>
      </div>
    </div>
    <DashboardCharts :clients="clientsStore.clients" :payments="paymentsStore.payments" />
    <div class="recent-section">
      <h2>Recent Payments</h2>
      <PaymentsTable
        :payments="paymentsStore.payments.slice(0, 10)"
        :pagination="{ count: 10, pageSize: 10, page: 1, next: null, previous: null }"
        @fetch="() => {}"
      />
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useClientsStore } from '../store/clients'
import { usePaymentsStore } from '../store/payments'
import DashboardCharts from '../components/DashboardCharts.vue'
import PaymentsTable from '../components/PaymentsTable.vue'

const clientsStore = useClientsStore()
const paymentsStore = usePaymentsStore()

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
  clientsStore.fetchClients({ page_size: 100 })
  paymentsStore.fetchPayments({ page_size: 100 })
})

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
</style>
