let socket = null
let reconnectInterval = null
const listeners = new Set()

const WS_URL = import.meta.env.VITE_WS_URL || `ws://${window.location.host}/ws/dashboard/`

export function connectWebSocket() {
  if (socket && (socket.readyState === WebSocket.OPEN || socket.readyState === WebSocket.CONNECTING)) {
    return
  }

  socket = new WebSocket(WS_URL)

  socket.onopen = () => {
    console.log('WebSocket connected')
    if (reconnectInterval) {
      clearInterval(reconnectInterval)
      reconnectInterval = null
    }
  }

  socket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data)
      listeners.forEach((cb) => cb(data))
    } catch (e) {
      console.error('WebSocket message parse error:', e)
    }
  }

  socket.onclose = () => {
    console.log('WebSocket disconnected')
    scheduleReconnect()
  }

  socket.onerror = (error) => {
    console.error('WebSocket error:', error)
  }
}

function scheduleReconnect() {
  if (!reconnectInterval) {
    reconnectInterval = setInterval(() => {
      console.log('WebSocket reconnecting...')
      connectWebSocket()
    }, 3000)
  }
}

export function disconnectWebSocket() {
  if (reconnectInterval) {
    clearInterval(reconnectInterval)
    reconnectInterval = null
  }
  if (socket) {
    socket.close()
    socket = null
  }
}

export function addWebSocketListener(callback) {
  listeners.add(callback)
  return () => listeners.delete(callback)
}

export function sendWebSocketMessage(data) {
  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify(data))
  }
}
