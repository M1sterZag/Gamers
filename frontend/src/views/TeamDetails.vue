<template>
  <div v-if="team" class="team-details pt-[88px] pr-[64px] pl-[2px]">
    <!-- Заголовок -->
    <h1 class="text-s32 font-bold mb-6">Приятного общения!</h1>

    <!-- Верхний ряд -->
    <div class="flex items-center gap-4 mb-6">
      <div class="bg-secondary p-4 rounded-lg flex-1">
        <h2 class="text-xl font-semibold">{{ team.name }}</h2>
      </div>

      <div class="bg-secondary p-4 rounded-lg flex-1">
        <p class="text-lg">Участники {{ team.members.length }}/{{ team.max_members }}</p>
      </div>

      <!-- Кнопки действий -->
      <button
          v-if="isOwner || isAdmin"
          class="bg-red-600 text-text py-3 px-4 rounded-lg font-semibold text-s20 hover:bg-red-700 transition"
          @click="openDeleteModal"
      >
        Удалить команду
      </button>

      <button
          class="bg-accent !text-secondary py-3 px-4 rounded-lg font-medium text-s20 hover:bg-accent_hover ml-4"
          @click="leaveTeam"
      >
        Покинуть
      </button>
    </div>

    <!-- Модальное окно для подтверждения удаления -->
    <div
        v-if="isDeleteModalOpen"
        class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50"
    >
      <div class="bg-fon p-8 rounded-brs w-full max-w-[500px]">
        <h2 class="text-2xl font-semibold text-text mb-4 text-center">
          Вы уверены, что хотите удалить команду?
        </h2>
        <p class="text-center text-text mb-6">
          Это действие нельзя отменить. Все связанные данные будут удалены.
        </p>
        <div class="flex justify-center gap-4">
          <button
              class="bg-red-600 text-text py-2 px-4 rounded-lg font-semibold text-s20 hover:bg-red-700 transition"
              @click="deleteTeam"
          >
            Да, удалить
          </button>
          <button
              class="bg-secondary !text-text py-2 px-4 rounded-lg font-semibold text-s20 hover:bg-secondary_hover transition"
              @click="closeDeleteModal"
          >
            Отмена
          </button>
        </div>
      </div>
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
      <div class="flex flex-col h-full border-4 border-secondary p-2 rounded-lg">
        <!--        <h3 class="text-lg font-semibold mb-4">Чат команды</h3>-->
        <Chat :team-id="team.id"/>
      </div>
    </div>
  </div>

  <div v-else class="text-center py-10">
    <p>Загрузка данных команды...</p>
  </div>
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

// Проверка, является ли текущий пользователь владельцем команды
const isOwner = computed(() => {
  return team.value?.owner_id === authStore.user.id;
});

// Проверка, является ли текущий пользователь администратором
const isAdmin = computed(() => {
  return authStore.user?.is_admin;
});

const formatDate = (dateStr) => {
  const date = new Date(dateStr);
  return date.toLocaleDateString('ru-RU');
};

const formattedTime = (dateStr) => {
  const date = new Date(dateStr);
  return date.toLocaleTimeString('ru-RU', {hour: '2-digit', minute: '2-digit'});
};

// Загрузка данных команды
const fetchTeam = async () => {
  try {
    const response = await api.get(`/api/teams/${route.params.id}`);
    team.value = response.data;
  } catch (error) {
    console.error('Ошибка загрузки команды:', error);
    router.push('/teams');
  }
};

// Открытие модального окна удаления
const openDeleteModal = () => {
  isDeleteModalOpen.value = true;
};

// Закрытие модального окна удаления
const closeDeleteModal = () => {
  isDeleteModalOpen.value = false;
};

// Удаление команды
const deleteTeam = async () => {
  try {
    await api.delete(`/api/teams/${team.value.id}`);
    router.push('/teams'); // Перенаправление на страницу команд
  } catch (error) {
    console.error('Ошибка удаления команды:', error);
  }
};

// Покинуть команду
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