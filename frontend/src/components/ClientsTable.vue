<template>
  <div class="table-container">
    <div class="toolbar">
      <input v-model="search" placeholder="Поиск клиентов..." @input="debouncedSearch" />
      <button class="btn btn-primary" @click="$emit('create')">+ Новый клиент</button>
    </div>
    <table class="data-table">
      <thead>
        <tr>
          <th @click="setOrdering('id')">ID {{ sortIcon('id') }}</th>
          <th @click="setOrdering('first_name')">Имя {{ sortIcon('first_name') }}</th>
          <th @click="setOrdering('last_name')">Фамилия {{ sortIcon('last_name') }}</th>
          <th @click="setOrdering('country')">Страна {{ sortIcon('country') }}</th>
          <th>Платежи</th>
          <th>Сумма</th>
          <th class="actions-col">Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="client in clients" :key="client.id">
          <td>{{ client.id }}</td>
          <td>{{ client.first_name }}</td>
          <td>{{ client.last_name }}</td>
          <td>{{ client.country }}</td>
          <td>{{ client.payments_count }}</td>
          <td>{{ formatMoney(client.total_payments) }}</td>
          <td class="actions">
            <button class="btn-icon" @click="$emit('edit', client)" title="Редактировать">✎</button>
            <button class="btn-icon" @click="$emit('delete', client)" title="Удалить">🗑</button>
            <button class="btn-icon" @click="$router.push(`/clients/${client.id}`)" title="Просмотр">👁</button>
          </td>
        </tr>
        <tr v-if="clients.length === 0">
          <td colspan="7" class="empty">Клиенты не найдены</td>
        </tr>
      </tbody>
    </table>
    <div class="pagination" v-if="pagination.count > pagination.pageSize">
      <button :disabled="!pagination.previous" @click="changePage(-1)">← Назад</button>
      <span>Страница {{ pagination.page }} из {{ totalPages }}</span>
      <button :disabled="!pagination.next" @click="changePage(1)">Вперёд →</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  clients: { type: Array, required: true },
  pagination: { type: Object, required: true },
})

const emit = defineEmits(['create', 'edit', 'delete', 'fetch'])

const search = ref('')
const ordering = ref('id')
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
  padding: 10px 12px;
  border-bottom: 1px solid #f0f0f0;
}

.data-table tr:hover td {
  background: #fafafa;
}

.actions-col {
  width: 1px;
  white-space: nowrap;
}

.actions {
  display: flex;
  gap: 4px;
  white-space: nowrap;
}

.btn-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  background: #f0f2f5;
  border: 1px solid transparent;
  cursor: pointer;
  font-size: 0.9rem;
  border-radius: 6px;
  transition: all 0.15s ease;
  line-height: 1;
  color: #444;
}

.btn-icon:hover {
  background: #e4e6eb;
  border-color: #d0d4dc;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0,0,0,0.08);
}

.btn-icon:active {
  transform: translateY(0);
  box-shadow: none;
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
