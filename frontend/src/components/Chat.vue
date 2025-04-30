<template>
  <div class="flex flex-col h-full min-h-[300px]">
    <!-- Область сообщений -->
    <div class="flex-grow overflow-y-auto p-2 sm:p-4 space-y-4">
      <article
          v-for="(msg, index) in messages"
          :key="index"
          :class="[
          'flex w-full',
          msg.is_sender ? 'justify-end' : 'justify-start'
        ]"
      >
        <div
            :class="[
            'rounded-lg p-4 max-w-[80%] lg:max-w-[60%]',
            msg.is_sender ? 'bg-primary text-text' : 'bg-secondary text-text'
          ]"
        >
          <header>
            <strong>{{ msg.username }}</strong>
          </header>
          <p class="mt-1 text-sm sm:text-base">{{ msg.content }}</p>
          <footer class="text-xs text-text/80 mt-1 sm:mt-2">
            {{ msg.created_at }}
          </footer>
        </div>
      </article>
    </div>

    <!-- Форма отправки - измененная для мобильных устройств -->
    <form @submit.prevent="sendMessage" class="flex items-center p-2 sm:p-4 border-t-2 border-secondary gap-2">
      <input
          v-model="newMessage"
          placeholder="Введите сообщение..."
          class="flex-grow p-2 sm:p-3 rounded-lg bg-secondary text-text focus:outline-none focus:ring-2 focus:ring-primary text-sm sm:text-base"
      />
      <button
          type="submit"
          class="p-2 sm:p-3 bg-accent text-secondary rounded-lg hover:bg-accent_hover transition min-w-[40px] flex items-center justify-center"
          :disabled="!newMessage.trim()"
      >
        <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
        >
          <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
          />
        </svg>
      </button>
    </form>
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

const connectToChat = (teamId) => {
  socket = new WebSocket(`/ws/${teamId}`)

  socket.onmessage = (event) => {
    const messageData = JSON.parse(event.data)
    messages.value.push({
      content: messageData.content,
      username: messageData.username,
      created_at: messageData.created_at,
      is_sender: messageData.sender_id === authStore.user.id
    })
  }
}

const sendMessage = () => {
  if (socket?.readyState === WebSocket.OPEN && newMessage.value.trim()) {
    socket.send(newMessage.value)
    newMessage.value = ''
  }
}

onMounted(() => connectToChat(route.params.id))
onUnmounted(() => socket?.close())
</script>