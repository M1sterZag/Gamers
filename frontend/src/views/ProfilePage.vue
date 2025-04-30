<template>
  <main class="">
    <!-- Заголовок профиля и кнопка выхода -->
    <section class="flex flex-col xs:flex-row items-center justify-between gap-4 mb-5">
      <h1 class="text-3xl lg:text-5xl font-semibold text-text leading-tight">Профиль</h1>
      <button
          class="p-3 lg:p-4 bg-red-500 hover:bg-red-700 text-white rounded-lg transition block font-medium text-s20"
          @click="logout"
      >
        Выйти
      </button>
    </section>

    <!-- Аватар, никнейм и дата регистрации -->
    <section class="flex flex-col sm:flex-row items-center justify-center gap-4 mb-8">
      <div
          class="flex flex-col sm:flex-row items-center bg-secondary p-3 rounded-lg border-4 border-secondary w-full gap-2 sm:w-auto"
          :class="{ 'animate-neon-border': hasSubscription }">
        <!-- Аватар -->
        <div class="flex-shrink-0 w-16 h-16 lg:w-20 lg:h-20 rounded-full overflow-hidden relative">
          <img
              v-if="profileUser?.avatar"
              :src="profileUser.avatar"
              alt="Avatar"
              class="w-full h-full object-cover"
          />
          <div
              v-else
              class="w-full h-full bg-accent flex items-center justify-center text-secondary text-2xl lg:text-3xl font-bold"
          >
            {{ profileUser?.username.charAt(0).toUpperCase() }}
          </div>
        </div>
        <!-- Никнейм -->
        <span class="font-semibold text-xl lg:text-2xl sm:flex-grow">{{ profileUser?.username }}</span>
      </div>
      <!-- Дата регистрации -->
      <div class="bg-secondary p-3 rounded-lg w-full sm:w-auto">
        <p class="text-s16 lg:text-s20 text-text/80 mt-2">Зарегистрирован</p>
        <p class="text-s16 lg:text-s20 text-text/80">{{ profileUser?.created_at }}</p>
      </div>
    </section>

    <!-- Последние команды -->
    <section>
      <h2 class="text-2xl lg:text-4xl font-semibold text-text mb-6">Последние команды</h2>

      <div v-if="hasSubscription">
        <div v-if="recentTeams.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <div
              v-for="team in recentTeams"
              :key="team.id"
              class="bg-secondary text-text p-4 lg:p-6 rounded-lg border-2 border-secondary hover:border-accent"
          >
            <h4 class="text-lg lg:text-xl font-semibold mb-2">{{ team.name }}</h4>
            <p class="text-sm lg:text-base text-text/80">{{ team.game }}</p>
            <p class="text-sm lg:text-base text-text/80">{{ team.game_type }}</p>
            <p class="text-sm lg:text-base text-text/80">{{ team.description }}</p>
            <p class="text-sm lg:text-base text-text/80">{{ formatDate(team.time) }}</p>

            <div class="flex items-center mt-2">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                   class="w-6 h-6 text-text">
                <path fill="currentColor" fill-rule="evenodd"
                      d="M12 4a8 8 0 0 0-6.96 11.947A4.99 4.99 0 0 1 9 14h6a4.99 4.99 0 0 1 3.96 1.947A8 8 0 0 0 12 4m7.943 14.076q.188-.245.36-.502A9.96 9.96 0 0 0 22 12c0-5.523-4.477-10-10-10S2 6.477 2 12a9.96 9.96 0 0 0 2.057 6.076l-.005.018l.355.413A9.98 9.98 0 0 0 12 22q.324 0 .644-.02a9.95 9.95 0 0 0 5.031-1.745a10 10 0 0 0 1.918-1.728l.355-.413zM12 6a3 3 0 1 0 0 6a3 3 0 0 0 0-6"
                      clip-rule="evenodd"/>
              </svg>
              <span class="text-sm lg:text-base text-text ml-2">{{ team.members_count }}</span>
            </div>
          </div>
        </div>
        <p v-else class="text-sm lg:text-base text-text/80 italic">Нет последних команд</p>
      </div>

      <div v-else class="relative">
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-2 gap-4">
          <div
              v-for="i in 2"
              :key="i"
              class="text-text p-4 lg:p-6 rounded-lg bg-fon blur-sm"
          >
            <h4 class="text-lg lg:text-xl font-semibold mb-2">Команда {{ i }}</h4>
            <p class="text-sm lg:text-base text-text/80">Игра</p>
            <p class="text-sm lg:text-base text-text/80">Дата и время</p>
            <div class="flex items-center mt-2">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                   class="w-6 h-6 text-text">
                <path fill="currentColor" fill-rule="evenodd"
                      d="M12 4a8 8 0 0 0-6.96 11.947A4.99 4.99 0 0 1 9 14h6a4.99 4.99 0 0 1 3.96 1.947A8 8 0 0 0 12 4m7.943 14.076q.188-.245.36-.502A9.96 9.96 0 0 0 22 12c0-5.523-4.477-10-10-10S2 6.477 2 12a9.96 9.96 0 0 0 2.057 6.076l-.005.018l.355.413A9.98 9.98 0 0 0 12 22q.324 0 .644-.02a9.95 9.95 0 0 0 5.031-1.745a10 10 0 0 0 1.918-1.728l.355-.413zM12 6a3 3 0 1 0 0 6a3 3 0 0 0 0-6"
                      clip-rule="evenodd"/>
              </svg>
              <span class="text-sm lg:text-base text-text ml-2">5 участников</span>
            </div>
          </div>
        </div>
        <div class="absolute inset-0 flex items-center justify-center">
          <div class="bg-secondary/80 p-4 rounded-lg text-center">
            <p class="text-sm lg:text-base font-semibold">Доступно с подпиской Gamers+</p>
            <router-link
                to="/premium"
                class="mt-2 inline-block bg-accent text-secondary py-2 px-4 rounded-lg font-medium text-sm lg:text-base hover:bg-accent_hover"
            >
              Оформить подписку
            </router-link>
          </div>
        </div>
      </div>
    </section>
  </main>
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
    profileUser.value = authStore.user;
    await subscriptionStore.checkCurrentSubscription();
    await loadRecentTeams();
  } catch (error) {
    console.error('Ошибка загрузки данных профиля:', error);
  } finally {
    isLoading.value = false;
  }
});
</script>