<template>
  <div class="page">
    <h1>Payments</h1>
    <PaymentsTable
      :payments="paymentsStore.payments"
      :pagination="paymentsStore.pagination"
      @fetch="handleFetch"
      @create="openModal()"
      @edit="openModal"
      @delete="handleDelete"
    />

    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <h2>{{ isEdit ? 'Edit Payment' : 'New Payment' }}</h2>
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
import { ref, onMounted } from 'vue'
import { useClientsStore } from '../store/clients'
import { usePaymentsStore } from '../store/payments'
import PaymentsTable from '../components/PaymentsTable.vue'
import PaymentForm from '../components/PaymentForm.vue'

const clientsStore = useClientsStore()
const paymentsStore = usePaymentsStore()
const showModal = ref(false)
const selectedPayment = ref(null)
const isEdit = ref(false)

onMounted(() => {
  paymentsStore.fetchPayments()
  clientsStore.fetchClients({ page_size: 1000 })
})

function handleFetch(params) {
  if (params.page) paymentsStore.setPage(params.page)
  paymentsStore.fetchPayments(params)
}

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

async function handleDelete(payment) {
  if (!confirm(`Delete payment #${payment.id}?`)) return
  try {
    await paymentsStore.deletePayment(payment.id)
  } catch (e) {}
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
  max-width: 520px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.2);
}

.modal h2 {
  margin-bottom: 16px;
  font-size: 1.25rem;
}
</style>
