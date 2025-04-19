<template>
  <div class="flex flex-col h-full">
    <!-- Область для отображения сообщений -->
    <div class="flex-grow overflow-y-auto p-4 space-y-2">
      <div
          v-for="(msg, index) in messages"
          :key="index"
          :class="[
            'message rounded-lg p-4 max-w-4/5',
            msg.is_sender ? 'bg-accent text-secondary self-end' : 'bg-secondary text-text self-start'
          ]"
      >
        <strong>{{ msg.sender }}:</strong> {{ msg.content }}
        <div class="text-s12 text-text/60 mt-1">{{ msg.time }}</div>
      </div>
    </div>

    <!-- Поле ввода и кнопка отправки -->
    <div class="flex items-center p-4">
      <input
          v-model="newMessage"
          @keyup.enter="sendMessage"
          placeholder="Введите сообщение..."
          class="w-full p-2 rounded-brs !bg-secondary focus:outline-none focus:outline-accent border-2 border-secondary"
      />
      <button
          @click="sendMessage"
          class="ml-2 p-2 bg-accent hover:bg-accent_hover !text-secondary rounded-brs transition"
      >
        <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
        >
          <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M14 5l7 7m0 0l-7 7m7-7H3"
          />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import {ref, onMounted, onUnmounted} from 'vue'
import {useRoute} from 'vue-router'
import {useAuthStore} from '@/stores/auth.js'

const route = useRoute()
const authStore = useAuthStore()
const messages = ref([])
const newMessage = ref('')
let socket = null

// Функция подключения к чату
const connectToChat = (teamId) => {
  socket = new WebSocket(`ws://localhost:8000/ws/chats/${teamId}`)

  socket.onopen = () => {
    console.log('WebSocket connected')
  }

  socket.onmessage = (event) => {
    // Парсим входящее сообщение из JSON
    const messageData = JSON.parse(event.data)

    // Добавляем сообщение в массив
    messages.value.push({
      content: messageData.content,
      sender: messageData.is_sender ? 'You' : 'Other',
      time: messageData.created_at,
      is_sender: messageData.is_sender
    })
  }

  socket.onerror = (error) => {
    console.error('WebSocket error:', error)
  }

  socket.onclose = () => {
    console.log('WebSocket disconnected')
  }
}

// Функция отправки сообщения
const sendMessage = () => {
  if (socket && socket.readyState === WebSocket.OPEN && newMessage.value.trim()) {
    socket.send(newMessage.value)
    newMessage.value = ''
  }
}

// Подключение к чату при монтировании компонента
onMounted(() => {
  connectToChat(route.params.id)
})

// Закрытие соединения при размонтировании компонента
onUnmounted(() => {
  if (socket) {
    socket.close()
  }
})
</script>

<style>
</style>