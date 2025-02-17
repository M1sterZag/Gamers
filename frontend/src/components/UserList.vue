<script setup>
    import { ref, onMounted } from "vue";

    const users = ref([]);

    onMounted(async () => {
    const response = await fetch("http://127.0.0.1:8000/api/users/");
    users.value = await response.json();
    });
</script>

<template>
  <div class="p-4">
    <h1 class="text-xl font-bold">Users</h1>
    <ul>
      <li v-for="user in users" :key="user.id">
        {{ user.username }} ({{ user.email }})
      </li>
    </ul>
  </div>
</template>
