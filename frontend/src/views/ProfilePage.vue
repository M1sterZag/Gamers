<template>
  <div class="pt-[88px] px-[30px] text-text">
    <h1 class="text-left text-[48px] font-semibold">Профиль</h1>

    <!-- Аватар, никнейм и кнопка выхода -->
    <div class="flex items-center mt-3">
      <div
          class="flex items-center bg-secondary p-3 rounded-lg mr-2"
          :class="{ 'animate-neon-border border-secondary border-4': hasSubscription }"
      >
        <div class="w-16 h-16 rounded-full overflow-hidden relative">
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
        <span
            class="font-semibold text-[24px] ml-2"
        >
          {{ profileUser?.username }}
        </span>
      </div>
      <button
          class="p-3 bg-red-500 hover:bg-red-700 text-text rounded-lg transition block font-semibold"
          @click="logout"
      >
        Выйти
      </button>
    </div>

    <!-- Последние команды -->
    <div class="mt-6">
      <h3 class="text-s32 font-semibold">Последние команды</h3>

      <div v-if="hasSubscription">
        <div v-if="recentTeams.length" class="mt-4 grid grid-cols-1 gap-4">
          <div
              v-for="team in recentTeams"
              :key="team.id"
              class="bg-fon text-text p-5 rounded-lg shadow-md border-2 border-secondary"
              :class="{ 'animate-neon-border': team.ownerHasSubscription }"
          >
            <h4 class="text-lg font-semibold">{{ team.name }}</h4>
            <p class="text-s16 text-text/80 mt-1">{{ team.game }}</p>
            <p class="text-s16 text-text/80 mt-1">{{ team.game_type }}</p>
            <p class="text-s16 text-text/80 mt-1">{{ team.description }}</p>
            <p class="text-s16 text-text/80 mt-1">{{ formatDate(team.time) }}</p>

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

      <div v-else class="relative mt-4">
        <div class="bg-fon text-text p-5 rounded-lg shadow-md blur-sm">
          <h4 class="text-lg font-semibold">Команда 1</h4>
          <p class="text-s16 text-text/80 mt-1">Игра</p>
          <p class="text-s16 text-text/80 mt-1">Дата и время</p>
          <div class="flex items-center mt-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                 class="w-[27px] h-[27px] text-text">
              <path fill="currentColor" fill-rule="evenodd"
                    d="M12 4a8 8 0 0 0-6.96 11.947A4.99 4.99 0 0 1 9 14h6a4.99 4.99 0 0 1 3.96 1.947A8 8 0 0 0 12 4m7.943 14.076q.188-.245.36-.502A9.96 9.96 0 0 0 22 12c0-5.523-4.477-10-10-10S2 6.477 2 12a9.96 9.96 0 0 0 2.057 6.076l-.005.018l.355.413A9.98 9.98 0 0 0 12 22q.324 0 .644-.02a9.95 9.95 0 0 0 5.031-1.745a10 10 0 0 0 1.918-1.728l.355-.413zM12 6a3 3 0 1 0 0 6a3 3 0 0 0 0-6"
                    clip-rule="evenodd"/>
            </svg>
            <span class="text-s16 text-text ml-2">5 участников</span>
          </div>
        </div>
        <div class="bg-fon text-text p-5 rounded-lg shadow-md blur-sm">
          <h4 class="text-lg font-semibold">Команда 1</h4>
          <p class="text-s16 text-text/80 mt-1">Игра</p>
          <p class="text-s16 text-text/80 mt-1">Дата и время</p>
          <div class="flex items-center mt-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                 class="w-[27px] h-[27px] text-text">
              <path fill="currentColor" fill-rule="evenodd"
                    d="M12 4a8 8 0 0 0-6.96 11.947A4.99 4.99 0 0 1 9 14h6a4.99 4.99 0 0 1 3.96 1.947A8 8 0 0 0 12 4m7.943 14.076q.188-.245.36-.502A9.96 9.96 0 0 0 22 12c0-5.523-4.477-10-10-10S2 6.477 2 12a9.96 9.96 0 0 0 2.057 6.076l-.005.018l.355.413A9.98 9.98 0 0 0 12 22q.324 0 .644-.02a9.95 9.95 0 0 0 5.031-1.745a10 10 0 0 0 1.918-1.728l.355-.413zM12 6a3 3 0 1 0 0 6a3 3 0 0 0 0-6"
                    clip-rule="evenodd"/>
            </svg>
            <span class="text-s16 text-text ml-2">5 участников</span>
          </div>
        </div>
        <div class="absolute inset-0 flex items-center justify-center">
          <div class="bg-secondary/90 p-4 rounded-lg text-center">
            <p class="text-lg font-semibold">Доступно с подпиской Gamers+</p>
            <router-link
                to="/premium"
                class="mt-2 inline-block bg-accent text-secondary py-2 px-4 rounded-lg font-medium hover:bg-accent_hover"
            >
              Оформить подписку
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, onMounted, computed} from 'vue';
import {useRoute, useRouter} from 'vue-router';
import {useAuthStore} from '../stores/auth';
import {useSubscriptionStore} from '../stores/subscriptionStore';
import api from '../api';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const subscriptionStore = useSubscriptionStore();

const profileUser = ref(null);
const recentTeams = ref([]);
const isLoading = ref(true);

const hasSubscription = computed(() => {
  return !!subscriptionStore.currentSubscriptionId;
});

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

const loadRecentTeams = async () => {
  try {
    if (hasSubscription.value) {
      const response = await api.get(`/api/teams/recent/${profileUser.value.id}`);
      recentTeams.value = response.data.map(team => ({
        ...team,
        formattedTime: formatDate(team.time),
      }));
    }
  } catch (error) {
    console.error('Ошибка загрузки последних команд:', error);
  }
};

onMounted(async () => {
  await authStore.checkAuth();
  if (!authStore.isAuthenticated) {
    router.push('/login');
    return;
  }

  const userId = route.params.id;
  const isOwnProfile = !userId || userId === authStore.user.id;

  try {
    profileUser.value = isOwnProfile ? authStore.user : (await api.get(`/api/users/${userId}`)).data;
    await subscriptionStore.checkCurrentSubscription();
    await loadRecentTeams();
  } catch (error) {
    console.error('Ошибка загрузки данных профиля:', error);
  } finally {
    isLoading.value = false;
  }
});
</script>