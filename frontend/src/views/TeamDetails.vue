<template>
  <div v-if="team" class="team-details pt-[88px] pr-[64px] pl-[2px]">
    <!-- Заголовок -->
    <h1 class="text-3xl font-bold mb-6">Приятного общения!</h1>

    <!-- Верхний ряд -->
    <div class="flex items-center gap-4 mb-6">
      <div class="bg-secondary p-4 rounded-lg flex-1">
        <h2 class="text-xl font-semibold">{{ team.name }}</h2>
      </div>
      <div class="bg-secondary p-4 rounded-lg flex-1">
        <p class="text-lg">Участники {{ team.members.length }}/{{ team.max_members }}</p>
      </div>
      <button
          class="bg-accent !text-secondary py-3 px-4 rounded-lg font-medium text-s20 hover:bg-accent_hover ml-4"
          @click="leaveTeam">
        Покинуть
      </button>
    </div>

    <!-- Две колонки -->
    <div class="grid grid-cols-1 lg:grid-cols-[auto_minmax(0,_1fr)] gap-6">
      <!-- Левая колонка -->
      <div class="space-y-4">
        <div class="grid gap-4 auto-cols-min">
          <div class="bg-secondary p-4 rounded-lg">
            <h3 class="text-lg font-semibold mb-2">Описание команды</h3>
            <p>{{ team.description }}</p>
          </div>

          <div class="bg-secondary p-4 rounded-lg">
            <h3 class="text-lg font-semibold mb-2">Название игры</h3>
            <p>{{ team.game }}</p>
          </div>

          <div class="bg-secondary p-4 rounded-lg">
            <h3 class="text-lg font-semibold mb-2">Тип игры</h3>
            <p>{{ team.gameType }}</p>
          </div>

          <!-- Дата и время -->
          <div class="flex gap-4">
            <div class="bg-secondary p-4 rounded-lg">
              <h3 class="text-lg font-semibold mb-2">Дата</h3>
              <p>{{ formatDate(team.time) }}</p>
            </div>
            <div class="bg-secondary p-4 rounded-lg">
              <h3 class="text-lg font-semibold mb-2">Время</h3>
              <p>{{ formattedTime(team.time) }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Правая колонка (чат) -->
      <div class="flex flex-col h-full">
        <h3 class="text-lg font-semibold mb-4">Чат команды</h3>
        <div class="bg-tertiary rounded-lg p-4 flex-grow flex items-center justify-center">
          <p class="text-text/80">Компонент чата будет здесь</p>
        </div>
      </div>
    </div>
  </div>
  <div v-else class="text-center py-10">
    <p>Загрузка данных команды...</p>
  </div>
</template>

<script setup>
import {ref, onMounted} from 'vue';
import {useRoute, useRouter} from 'vue-router';
import {useAuthStore} from '../stores/auth';
import api from '../api';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const team = ref(null);

const formatDate = (dateStr) => {
  const date = new Date(dateStr);
  return date.toLocaleDateString('ru-RU');
};

const formattedTime = (dateStr) => {
  const date = new Date(dateStr);
  return date.toLocaleTimeString('ru-RU', {hour: '2-digit', minute: '2-digit'});
};

const fetchTeam = async () => {
  try {
    const response = await api.get(`/api/teams/${route.params.id}`);
    team.value = response.data;
  } catch (error) {
    console.error('Ошибка загрузки команды:', error);
    router.push('/teams');
  }
};

const leaveTeam = async () => {
  if (confirm('Вы уверены, что хотите покинуть команду?')) {
    try {
      await api.delete(`/api/teams/member/${route.params.id}`);
      router.push('/teams');
    } catch (error) {
      console.error('Ошибка при выходе из команды:', error);
    }
  }
};

onMounted(fetchTeam);
</script>

<style>
</style>