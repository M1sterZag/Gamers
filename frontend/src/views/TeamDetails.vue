<template>
  <main class="">
    <template v-if="team">
      <header class="mb-6 lg:mb-8">
        <div class="flex flex-col lg:flex-row justify-between xs:items-center items-start gap-4 mb-4 lg:mb-6">
          <h1 class="text-2xl lg:text-4xl font-bold text-text">
            Приятного общения!
          </h1>

          <div class="flex flex-col xs:flex-row gap-2 lg:gap-4">
            <button
                v-if="isOwner || isAdmin"
                class="bg-red-600 text-white py-2 px-2 rounded-lg font-semibold text-base lg:text-lg hover:bg-red-700 transition whitespace-nowrap"
                @click="openDeleteModal"
            >
              Удалить команду
            </button>

            <button
                class="bg-accent text-secondary py-2 px-2 rounded-lg font-medium text-base lg:text-lg hover:bg-accent_hover transition whitespace-nowrap"
                @click="leaveTeam"
            >
              Покинуть
            </button>
          </div>
        </div>

        <div class="flex flex-col sm:flex-row gap-4">
          <div class="bg-secondary p-4 rounded-lg flex-1">
            <h2 class="text-lg lg:text-xl font-semibold">{{ team.name }}</h2>
          </div>

          <div class="bg-secondary p-4 rounded-lg flex-1">
            <p class="text-base lg:text-lg">
              Участники {{ team.members.length }}/{{ team.max_members }}
            </p>
          </div>
        </div>
      </header>

      <!-- Остальной код остается без изменений -->
      <div class="grid grid-cols-1 lg:grid-cols-[1fr_2fr] gap-6">
        <!-- Левая колонка -->
        <section class="space-y-4">
          <article class="bg-secondary p-4 rounded-lg">
            <h3 class="text-lg font-semibold mb-2">Описание команды</h3>
            <p class="line-clamp-4">{{ team.description }}</p>
          </article>

          <article class="bg-secondary p-4 rounded-lg">
            <h3 class="text-lg font-semibold mb-2">Название игры</h3>
            <p>{{ team.game }}</p>
          </article>

          <article class="bg-secondary p-4 rounded-lg">
            <h3 class="text-lg font-semibold mb-2">Тип игры</h3>
            <p>{{ team.gameType }}</p>
          </article>

          <div class="grid grid-cols-2 gap-4">
            <article class="bg-secondary p-4 rounded-lg">
              <h3 class="text-lg font-semibold mb-2">Дата</h3>
              <p>{{ formatDate(team.time) }}</p>
            </article>

            <article class="bg-secondary p-4 rounded-lg">
              <h3 class="text-lg font-semibold mb-2">Время</h3>
              <p>{{ formattedTime(team.time) }}</p>
            </article>
          </div>
        </section>

        <!-- Правая колонка (чат) -->
        <section class="flex flex-col h-full border-2 border-secondary rounded-lg overflow-hidden">
          <Chat :team-id="team.id" class="flex-grow"/>
        </section>
      </div>

      <!-- Модальное окно удаления -->
      <div
          v-if="isDeleteModalOpen"
          class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50 p-4"
      >
        <article class="bg-fon p-6 rounded-lg w-full max-w-md">
          <header class="mb-4">
            <h2 class="text-xl lg:text-2xl font-semibold text-text text-center">
              Вы уверены, что хотите удалить команду?
            </h2>
          </header>

          <p class="text-center text-text mb-6">
            Это действие нельзя отменить. Все связанные данные будут удалены.
          </p>

          <footer class="flex justify-center gap-4">
            <button
                class="bg-red-600 text-white py-2 px-4 rounded-lg font-semibold hover:bg-red-700 transition"
                @click="deleteTeam"
            >
              Да, удалить
            </button>
            <button
                class="bg-secondary hover:bg-secondary_hover text-text py-2 px-4 rounded-lg font-semibold transition"
                @click="closeDeleteModal"
            >
              Отмена
            </button>
          </footer>
        </article>
      </div>
    </template>

    <div v-else class="flex items-center justify-center min-h-[60vh]">
      <p class="text-lg text-text">Загрузка данных команды...</p>
    </div>
  </main>
</template>

<script setup>
import {ref, onMounted, computed} from 'vue';
import {useRoute, useRouter} from 'vue-router';
import {useAuthStore} from '../stores/auth';
import api from '../api';
import Chat from "@/components/Chat.vue";

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const team = ref(null);
const isDeleteModalOpen = ref(false);

const isOwner = computed(() => team.value?.owner_id === authStore.user.id);
const isAdmin = computed(() => authStore.user?.is_admin);

const formatDate = (dateStr) => new Date(dateStr).toLocaleDateString('ru-RU');
const formattedTime = (dateStr) => new Date(dateStr).toLocaleTimeString('ru-RU', {hour: '2-digit', minute: '2-digit'});

const fetchTeam = async () => {
  try {
    const response = await api.get(`/api/teams/${route.params.id}`);
    team.value = response.data;
  } catch (error) {
    console.error('Ошибка загрузки команды:', error);
    router.push('/teams');
  }
};

const openDeleteModal = () => isDeleteModalOpen.value = true;
const closeDeleteModal = () => isDeleteModalOpen.value = false;

const deleteTeam = async () => {
  try {
    await api.delete(`/api/teams/${team.value.id}`);
    router.push('/teams');
  } catch (error) {
    console.error('Ошибка удаления команды:', error);
  }
};

const leaveTeam = async () => {
  if (confirm('Вы уверены, что хотите покинуть команду?')) {
    try {
      await api.delete(`/api/teams/member/${team.value.id}`);
      router.push('/teams');
    } catch (error) {
      console.error('Ошибка при выходе из команды:', error);
    }
  }
};

onMounted(fetchTeam);
</script>