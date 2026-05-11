import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import ClientsView from '../views/ClientsView.vue'
import ClientDetailView from '../views/ClientDetailView.vue'
import PaymentsView from '../views/PaymentsView.vue'
import PaymentDetailView from '../views/PaymentDetailView.vue'

const routes = [
  { path: '/', name: 'Dashboard', component: DashboardView },
  { path: '/clients', name: 'Clients', component: ClientsView },
  { path: '/clients/:id', name: 'ClientDetail', component: ClientDetailView, props: true },
  { path: '/payments', name: 'Payments', component: PaymentsView },
  { path: '/payments/:id', name: 'PaymentDetail', component: PaymentDetailView, props: true },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
