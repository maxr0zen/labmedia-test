<template>
  <div class="page">
    <h1>Clients</h1>
    <ClientsTable
      :clients="clientsStore.clients"
      :pagination="clientsStore.pagination"
      @fetch="handleFetch"
      @create="openModal()"
      @edit="openModal"
      @delete="handleDelete"
    />

    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <h2>{{ isEdit ? 'Edit Client' : 'New Client' }}</h2>
        <ClientForm
          :client="selectedClient"
          :loading="clientsStore.loading"
          @submit="handleSubmit"
          @cancel="closeModal"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useClientsStore } from '../store/clients'
import ClientsTable from '../components/ClientsTable.vue'
import ClientForm from '../components/ClientForm.vue'

const clientsStore = useClientsStore()
const showModal = ref(false)
const selectedClient = ref(null)
const isEdit = ref(false)

onMounted(() => {
  clientsStore.fetchClients()
})

function handleFetch(params) {
  if (params.page) clientsStore.setPage(params.page)
  clientsStore.fetchClients(params)
}

function openModal(client = null) {
  selectedClient.value = client
  isEdit.value = !!client
  showModal.value = true
}

function closeModal() {
  showModal.value = false
  selectedClient.value = null
}

async function handleSubmit(data) {
  try {
    if (isEdit.value) {
      await clientsStore.updateClient(selectedClient.value.id, data)
    } else {
      await clientsStore.createClient(data)
    }
    closeModal()
  } catch (e) {
    // errors handled in store
  }
}

async function handleDelete(client) {
  if (!confirm(`Delete client ${client.first_name} ${client.last_name}?`)) return
  try {
    await clientsStore.deleteClient(client.id)
  } catch (e) {
    // errors handled in store
  }
}
</script>

<style scoped>
.page {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

h1 {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1a237e;
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
  font-size: 1.25rem;
}
</style>
