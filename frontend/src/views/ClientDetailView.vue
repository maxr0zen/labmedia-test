<template>
  <div class="page">
    <div class="header">
      <button class="btn-back" @click="$router.back()">← Back</button>
      <h1>Client #{{ id }}</h1>
    </div>
    <div v-if="clientsStore.loading" class="loading">Loading...</div>
    <div v-else-if="clientsStore.client" class="detail-card">
      <div class="detail-grid">
        <div><strong>First Name:</strong> {{ clientsStore.client.first_name }}</div>
        <div><strong>Last Name:</strong> {{ clientsStore.client.last_name }}</div>
        <div><strong>Country:</strong> {{ clientsStore.client.country }}</div>
        <div><strong>Payments Count:</strong> {{ clientsStore.client.payments_count }}</div>
        <div><strong>Total Payments:</strong> {{ formatMoney(clientsStore.client.total_payments) }}</div>
      </div>
      <div class="actions">
        <button class="btn btn-primary" @click="showEdit = true">Edit</button>
        <button class="btn btn-danger" @click="handleDelete">Delete</button>
      </div>
    </div>

    <div v-if="showEdit" class="modal-overlay" @click.self="showEdit = false">
      <div class="modal">
        <h2>Edit Client</h2>
        <ClientForm
          :client="clientsStore.client"
          :loading="clientsStore.loading"
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
import { useClientsStore } from '../store/clients'
import ClientForm from '../components/ClientForm.vue'

const props = defineProps({ id: { type: String, required: true } })
const router = useRouter()
const clientsStore = useClientsStore()
const showEdit = ref(false)

onMounted(() => {
  clientsStore.fetchClient(props.id)
})

async function handleUpdate(data) {
  try {
    await clientsStore.updateClient(props.id, data)
    showEdit.value = false
  } catch (e) {}
}

async function handleDelete() {
  if (!confirm('Delete this client?')) return
  try {
    await clientsStore.deleteClient(props.id)
    router.push('/clients')
  } catch (e) {}
}

function formatMoney(val) {
  if (!val) return '$0.00'
  return '$' + Number(val).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
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
  max-width: 480px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.2);
}

.modal h2 {
  margin-bottom: 16px;
}
</style>
