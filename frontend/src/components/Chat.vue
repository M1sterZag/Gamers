<template>
  <div>
    <div v-for="msg in messages" :key="msg.id" class="message">
      {{ msg.content }}
    </div>
    <input v-model="newMessage" @keyup.enter="sendMessage" placeholder="Введите сообщение..."/>
  </div>
</template>

<script>
import {ref, onMounted, onUnmounted} from "vue";
import {connectToChat} from "../api/chat";

export default {
  props: {
    teamId: Number,
  },
  setup(props) {
    const messages = ref([]);
    const newMessage = ref("");
    let socket = null;

    const sendMessage = () => {
      if (socket && newMessage.value.trim() !== "") {
        socket.send(newMessage.value);
        newMessage.value = "";
      }
    };

    onMounted(() => {
      socket = connectToChat(props.teamId, (msg) => {
        messages.value.push({content: msg});
      });
    });

    onUnmounted(() => {
      if (socket) {
        socket.close();
      }
    });

    return {messages, newMessage, sendMessage};
  },
};
</script>

<style>
.message {
  padding: 8px;
  border-bottom: 1px solid #ddd;
}
</style>
