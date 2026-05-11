import { defineStore } from 'pinia'
import { clientsApi } from '../api'

export const useClientsStore = defineStore('clients', {
  state: () => ({
    clients: [],
    client: null,
    loading: false,
    error: null,
    pagination: {
      count: 0,
      next: null,
      previous: null,
      page: 1,
      pageSize: 20,
    },
  }),

  actions: {
    async fetchClients(params = {}) {
      this.loading = true
      this.error = null
      try {
        const response = await clientsApi.list({ page: this.pagination.page, page_size: this.pagination.pageSize, ...params })
        this.clients = response.data.results || response.data
        this.pagination.count = response.data.count || this.clients.length
        this.pagination.next = response.data.next
        this.pagination.previous = response.data.previous
      } catch (err) {
        this.error = err.response?.data?.detail || err.message
      } finally {
        this.loading = false
      }
    },

    async fetchClient(id) {
      this.loading = true
      this.error = null
      try {
        const response = await clientsApi.get(id)
        this.client = response.data
      } catch (err) {
        this.error = err.response?.data?.detail || err.message
      } finally {
        this.loading = false
      }
    },

    async createClient(data) {
      this.loading = true
      this.error = null
      try {
        const response = await clientsApi.create(data)
        this.clients.unshift(response.data)
        return response.data
      } catch (err) {
        this.error = err.response?.data || err.message
        throw err
      } finally {
        this.loading = false
      }
    },

    async updateClient(id, data) {
      this.loading = true
      this.error = null
      try {
        const response = await clientsApi.update(id, data)
        const idx = this.clients.findIndex((c) => c.id === id)
        if (idx !== -1) this.clients[idx] = response.data
        if (this.client?.id === id) this.client = response.data
        return response.data
      } catch (err) {
        this.error = err.response?.data || err.message
        throw err
      } finally {
        this.loading = false
      }
    },

    async deleteClient(id) {
      this.loading = true
      this.error = null
      try {
        await clientsApi.delete(id)
        this.clients = this.clients.filter((c) => c.id !== id)
        if (this.client?.id === id) this.client = null
      } catch (err) {
        this.error = err.response?.data?.detail || err.message
        throw err
      } finally {
        this.loading = false
      }
    },

    setPage(page) {
      this.pagination.page = page
    },
  },
})
