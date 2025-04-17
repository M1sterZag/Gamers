<template>
  <div v-if="isLoading" class="min-h-screen flex items-center justify-center">
    <p>Загрузка...</p>
  </div>
  <div v-else-if="!authStore.isAuthenticated" class="flex items-center justify-center">
    <p>Пожалуйста, войдите в систему.
      <router-link to="/login" class="text-primary hover:underline">Вход</router-link>
    </p>
  </div>
  <div v-else class="pt-[88px] px-[20px] text-text">
    <h1 class="text-left text-[48px] font-semibold">Профиль</h1>

    <!-- Аватар, никнейм и кнопка выхода -->
    <div class="flex items-center mt-3">
      <div class="items-center bg-secondary p-3 rounded-lg mr-2">
        <div class="w-16 h-16 rounded-full overflow-hidden">
          <img
              v-if="profileUser?.avatar"
              :src="profileUser.avatar"
              alt="Avatar"
              class="w-full h-full object-cover"
          />
          <div v-else
               class="w-full h-full bg-accent flex items-center justify-center text-secondary text-2xl font-bold">
            {{ profileUser?.username.charAt(0).toUpperCase() }}
          </div>
        </div>
        <span class="font-semibold text-[24px] text-primary">{{ profileUser?.username }}</span>
      </div>
      <button
          class="bg-red-500 text-secondary py-2 px-4 rounded-lg font-medium text-[16px] hover:bg-red-600"
          @click="logout">
        Выйти
      </button>
    </div>

    <!-- Последние команды -->
    <div class="mt-6">
      <h3 class="text-s32 font-semibold">Последние команды</h3>
      <div v-if="recentTeams.length" class="mt-4 grid grid-cols-1 gap-4">
        <div v-for="team in recentTeams" :key="team.id" class="bg-fon text-text p-5 rounded-lg shadow-md">
          <h4 class="text-lg font-semibold">{{ team.name }}</h4>
          <p class="text-s16 text-text/80 mt-1">{{ team.game }}</p>
          <p class="text-s16 text-text/80 mt-1">{{ formatDate(team.time) }}</p>

          <!-- Иконка пользователей и количество участников -->
          <div class="flex items-center mt-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                 class="w-[27px] h-[27px] text-text">
              <path fill="currentColor" fill-rule="evenodd"
                    d="M12 4a8 8 0 0 0-6.96 11.947A4.99 4.99 0 0 1 9 14h6a4.99 4.99 0 0 1 3.96 1.947A8 8 0 0 0 12 4m7.943 14.076q.188-.245.36-.502A9.96 9.96 0 0 0 22 12c0-5.523-4.477-10-10-10S2 6.477 2 12a9.96 9.96 0 0 0 2.057 6.076l-.005.018l.355.413A9.98 9.98 0 0 0 12 22q.324 0 .644-.02a9.95 9.95 0 0 0 5.031-1.745a10 10 0 0 0 1.918-1.728l.355-.413zM12 6a3 3 0 1 0 0 6a3 3 0 0 0 0-6"
                    clip-rule="evenodd"/>
            </svg>
            <span class="text-s16 text-text ml-2">{{ team.members_count }}</span>
          </div>
        </div>
      </div>
      <p v-else class="text-s16 text-text/80 mt-2 italic">Нет последних команд</p>
    </div>
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

const profileUser = ref(null);
const recentTeams = ref([]);
const isLoading = ref(true);

const formatDate = (dateStr) => {
  const date = new Date(dateStr);
  return new Intl.DateTimeFormat('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date);
};

const logout = async () => {
  await authStore.logout();
  router.push('/login');
};

onMounted(async () => {
  await authStore.checkAuth();
  if (!authStore.isAuthenticated) {
    router.push('/login');
    return;
  }

  const userId = route.params.id;
  const isOwnProfile = !userId || userId == authStore.user.id;

  try {
    profileUser.value = isOwnProfile ? authStore.user : (await api.get(`/api/users/${userId}`)).data;
    recentTeams.value = (await api.get(`/api/teams/recent/${profileUser.value.id}`)).data;
  } catch (error) {
    console.error('Ошибка загрузки данных профиля:', error);
  } finally {
    isLoading.value = false;
  }
});
</script>
