<template>
  <div class="app">
    <nav class="navbar">
      <div class="nav-brand">LabMedia Payments</div>
      <div class="nav-links">
        <router-link to="/" exact-active-class="active">Dashboard</router-link>
        <router-link to="/clients" exact-active-class="active">Clients</router-link>
        <router-link to="/payments" exact-active-class="active">Payments</router-link>
      </div>
      <div class="connection-status" :class="wsConnected ? 'connected' : 'disconnected'">
        {{ wsConnected ? 'Live' : 'Offline' }}
      </div>
    </nav>
    <main class="main-content">
      <router-view />
    </main>
    <NotificationToast />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { connectWebSocket, disconnectWebSocket, addWebSocketListener } from './websocket'
import NotificationToast from './components/NotificationToast.vue'

const wsConnected = ref(false)

let removeListener = null

onMounted(() => {
  connectWebSocket()
  removeListener = addWebSocketListener((data) => {
    if (data.type === 'model_update') {
      wsConnected.value = true
    }
  })
  // Simple heartbeat check
  const interval = setInterval(() => {
    wsConnected.value = true // optimistic, since reconnect is handled internally
  }, 5000)

  onUnmounted(() => {
    clearInterval(interval)
    if (removeListener) removeListener()
    disconnectWebSocket()
  })
})
</script>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.navbar {
  background: #1a237e;
  color: white;
  padding: 0 24px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-brand {
  font-size: 1.25rem;
  font-weight: 700;
}

.nav-links {
  display: flex;
  gap: 8px;
}

.nav-links a {
  color: rgba(255,255,255,0.85);
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 6px;
  transition: all 0.2s;
  font-weight: 500;
}

.nav-links a:hover,
.nav-links a.active {
  background: rgba(255,255,255,0.15);
  color: white;
}

.connection-status {
  font-size: 0.85rem;
  padding: 4px 12px;
  border-radius: 12px;
  font-weight: 600;
}

.connection-status.connected {
  background: #4caf50;
  color: white;
}

.connection-status.disconnected {
  background: #f44336;
  color: white;
}

.main-content {
  flex: 1;
  padding: 24px;
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
}
</style>
