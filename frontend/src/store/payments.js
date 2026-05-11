import { defineStore } from 'pinia'
import { paymentsApi } from '../api'

export const usePaymentsStore = defineStore('payments', {
  state: () => ({
    payments: [],
    payment: null,
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
    async fetchPayments(params = {}) {
      this.loading = true
      this.error = null
      try {
        const response = await paymentsApi.list({ page: this.pagination.page, page_size: this.pagination.pageSize, ...params })
        this.payments = response.data.results || response.data
        this.pagination.count = response.data.count || this.payments.length
        this.pagination.next = response.data.next
        this.pagination.previous = response.data.previous
      } catch (err) {
        this.error = err.response?.data?.detail || err.message
      } finally {
        this.loading = false
      }
    },

    async fetchPayment(id) {
      this.loading = true
      this.error = null
      try {
        const response = await paymentsApi.get(id)
        this.payment = response.data
      } catch (err) {
        this.error = err.response?.data?.detail || err.message
      } finally {
        this.loading = false
      }
    },

    async createPayment(data) {
      this.loading = true
      this.error = null
      try {
        const response = await paymentsApi.create(data)
        this.payments.unshift(response.data)
        return response.data
      } catch (err) {
        this.error = err.response?.data || err.message
        throw err
      } finally {
        this.loading = false
      }
    },

    async updatePayment(id, data) {
      this.loading = true
      this.error = null
      try {
        const response = await paymentsApi.update(id, data)
        const idx = this.payments.findIndex((p) => p.id === id)
        if (idx !== -1) this.payments[idx] = response.data
        if (this.payment?.id === id) this.payment = response.data
        return response.data
      } catch (err) {
        this.error = err.response?.data || err.message
        throw err
      } finally {
        this.loading = false
      }
    },

    async deletePayment(id) {
      this.loading = true
      this.error = null
      try {
        await paymentsApi.delete(id)
        this.payments = this.payments.filter((p) => p.id !== id)
        if (this.payment?.id === id) this.payment = null
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
