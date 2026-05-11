<template>
  <div class="table-container">
    <div class="toolbar">
      <input v-model="search" placeholder="Search payments..." @input="debouncedSearch" />
      <button class="btn btn-primary" @click="$emit('create')">+ New Payment</button>
    </div>
    <table class="data-table">
      <thead>
        <tr>
          <th @click="setOrdering('id')">ID {{ sortIcon('id') }}</th>
          <th @click="setOrdering('payer__first_name')">Payer {{ sortIcon('payer__first_name') }}</th>
          <th @click="setOrdering('amount')">Amount {{ sortIcon('amount') }}</th>
          <th @click="setOrdering('percent')">% {{ sortIcon('percent') }}</th>
          <th @click="setOrdering('pay_date')">Date {{ sortIcon('pay_date') }}</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="payment in payments" :key="payment.id">
          <td>{{ payment.id }}</td>
          <td>
            <router-link :to="`/clients/${payment.payer}`" class="link">
              {{ payment.payer_details?.first_name }} {{ payment.payer_details?.last_name }}
            </router-link>
          </td>
          <td>{{ formatMoney(payment.amount) }}</td>
          <td>{{ payment.percent }}%</td>
          <td>{{ formatDate(payment.pay_date) }}</td>
          <td class="actions">
            <button class="btn-icon" @click="$emit('edit', payment)" title="Edit">✎</button>
            <button class="btn-icon" @click="$emit('delete', payment)" title="Delete">🗑</button>
            <button class="btn-icon" @click="$router.push(`/payments/${payment.id}`)" title="View">👁</button>
          </td>
        </tr>
        <tr v-if="payments.length === 0">
          <td colspan="6" class="empty">No payments found</td>
        </tr>
      </tbody>
    </table>
    <div class="pagination" v-if="pagination.count > pagination.pageSize">
      <button :disabled="!pagination.previous" @click="changePage(-1)">← Prev</button>
      <span>Page {{ pagination.page }} of {{ totalPages }}</span>
      <button :disabled="!pagination.next" @click="changePage(1)">Next →</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  payments: { type: Array, required: true },
  pagination: { type: Object, required: true },
})

const emit = defineEmits(['create', 'edit', 'delete', 'fetch'])

const search = ref('')
const ordering = ref('-pay_date')
let searchTimeout = null

const totalPages = computed(() => Math.ceil(props.pagination.count / props.pagination.pageSize) || 1)

function debouncedSearch() {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    emit('fetch', { search: search.value, ordering: ordering.value, page: 1 })
  }, 300)
}

function setOrdering(field) {
  ordering.value = ordering.value === field ? `-${field}` : field
  emit('fetch', { search: search.value, ordering: ordering.value, page: 1 })
}

function sortIcon(field) {
  if (ordering.value === field) return '▲'
  if (ordering.value === `-${field}`) return '▼'
  return ''
}

function changePage(delta) {
  const newPage = props.pagination.page + delta
  emit('fetch', { search: search.value, ordering: ordering.value, page: newPage })
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
.table-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  padding: 20px;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  gap: 12px;
}

.toolbar input {
  flex: 1;
  max-width: 320px;
  padding: 10px 14px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
}

.btn {
  padding: 10px 18px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}

.btn-primary {
  background: #1a237e;
  color: white;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
}

.data-table th {
  text-align: left;
  padding: 12px;
  border-bottom: 2px solid #e0e0e0;
  font-weight: 600;
  color: #555;
  cursor: pointer;
  user-select: none;
}

.data-table td {
  padding: 12px;
  border-bottom: 1px solid #f0f0f0;
}

.data-table tr:hover td {
  background: #fafafa;
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
  gap: 8px;
}

.btn-icon {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.1rem;
  padding: 4px;
  border-radius: 4px;
  transition: background 0.2s;
}

.btn-icon:hover {
  background: #eee;
}

.empty {
  text-align: center;
  color: #999;
  padding: 40px;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 16px;
}

.pagination button {
  padding: 8px 16px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 6px;
  cursor: pointer;
}

.pagination button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
</style>
