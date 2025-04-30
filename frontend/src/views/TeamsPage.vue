<template>
  <div v-if="authStore.isAuthenticated" class="pt-[88px] pr-[64px] pl-[2px]">
    <h1 class="text-left text-[48px] font-semibold text-text">Найдите свою идеальную команду!</h1>

    <div class="mt-[30px] flex items-center">
      <div class="relative w-full max-w-[700px] mr-[20px]">
        <svg class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-text"
             xmlns="http://www.w3.org/2000/svg"
             fill="none"
             viewBox="0 0 24 24"
             stroke-width="1.5"
             stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round"
                d="M21 21l-4.35-4.35M16.25 10.5a5.75 5.75 0 1 1-11.5 0 5.75 5.75 0 0 1 11.5 0z"/>
        </svg>
        <input
            type="text"
            v-model="searchQuery"
            placeholder="Поиск по названию, игре, типу..."
            class="w-full p-3 pl-10 text-s16 text-text rounded-lg bg-secondary focus:outline-none focus:ring-2 focus:ring-primary placeholder:text-text/50"
        />
      </div>
      <button
          class="bg-accent !text-secondary py-2 px-4 rounded-lg font-medium text-s20 hover:bg-accent_hover ml-4"
          @click="openCreateTeamForm"
          :title="!hasSubscription ? 'Без подписки можно создать команду до 5 участников' : ''">
        Создать
      </button>
    </div>

    <!-- Фильтры -->
    <div class="filters mt-6 grid grid-cols-2 lg:grid-cols-4 xl:grid-cols-5 gap-4 shadow-none">
      <select v-model="selectedGame"
              class="p-2 rounded bg-secondary text-text focus:ring-2 focus:ring-primary outline-none">
        <option value="">Все игры</option>
        <option v-for="game in games" :key="game.id" :value="game.id">{{ game.name }}</option>
      </select>
      <select v-model="selectedGameType"
              class="p-2 rounded bg-secondary text-text focus:ring-2 focus:ring-primary outline-none">
        <option value="">Все типы</option>
        <option v-for="type in gameTypes" :key="type.id" :value="type.id">{{ type.name }}</option>
      </select>
      <select v-model="selectedDate"
              class="p-2 rounded bg-secondary text-text focus:ring-2 focus:ring-primary outline-none">
        <option value="">Любая дата</option>
        <option value="today">Сегодня</option>
        <option value="week">Эта неделя</option>
        <option value="month">Этот месяц</option>
      </select>
      <select v-model="selectedPlayers"
              class="p-2 rounded bg-secondary text-text focus:ring-2 focus:ring-primary outline-none">
        <option value="">Любое кол-во</option>
        <option value="small">До 5</option>
        <option value="medium">От 5 до 10</option>
        <option value="large">Больше 10</option>
      </select>
      <label class="flex items-center p-2 rounded bg-secondary text-text">
        <input type="checkbox" v-model="onlyMyTeams" class="mr-2"/>
        Мои команды
      </label>
    </div>

    <div class="teams mt-10 grid grid-cols-1 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      <div v-for="team in filteredTeams" :key="team.id"
           class="team-card bg-secondary text-text p-5 rounded-lg shadow-md flex flex-col items-center text-center border-2 border-secondary"
           :class="{ 'animate-neon-border': team.ownerHasSubscription }">
        <h2 class="text-xl font-semibold">{{ team.name }}</h2>
        <p class="text-s16 text-text/80 mt-1">{{ team.game }}</p>
        <p class="text-s16 text-text/80 mt-1">{{ team.gameType }}</p>
        <p class="text-s16 text-text/80 mt-1">{{ team.formattedTime }}</p>
        <p class="text-s16 text-text/80 mt-2">{{ team.description }}</p>

        <!-- Отображение участников -->
        <div class="flex items-center mt-2 mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
               class="w-[28px] h-[28px] text-text">
            <path fill="currentColor" fill-rule="evenodd"
                  d="M12 4a8 8 0 0 0-6.96 11.947A4.99 4.99 0 0 1 9 14h6a4.99 4.99 0 0 1 3.96 1.947A8 8 0 0 0 12 4m7.943 14.076q.188-.245.36-.502A9.96 9.96 0 0 0 22 12c0-5.523-4.477-10-10-10S2 6.477 2 12a9.96 9.96 0 0 0 2.057 6.076l-.005.018l.355.413A9.98 9.98 0 0 0 12 22q.324 0 .644-.02a9.95 9.95 0 0 0 5.031-1.745a10 10 0 0 0 1.918-1.728l.355-.413zM12 6a3 3 0 1 0 0 6a3 3 0 0 0 0-6"
                  clip-rule="evenodd"/>
          </svg>
          <div class="flex">
            <template v-for="i in Math.min(team.max_members - 1, 4)" :key="i">
              <svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024"
                   class="w-[25px] h-[25px] text-accent ml-1">
                <path fill="currentColor"
                      d="M512 0C229.232 0 0 229.232 0 512c0 282.784 229.232 512 512 512c282.784 0 512-229.216 512-512C1024 229.232 794.784 0 512 0m0 961.008c-247.024 0-448-201.984-448-449.01c0-247.024 200.976-448 448-448s448 200.977 448 448s-200.976 449.01-448 449.01M736 480H544V288c0-17.664-14.336-32-32-32s-32 14.336-32 32v192H288c-17.664 0-32 14.336-32 32s14.336 32 32 32h192v192c0 17.664 14.336 32 32 32s32-14.336 32-32V544h192c17.664 0 32-14.336 32-32s-14.336-32-32-32"/>
              </svg>
            </template>
            <span v-if="team.max_members > 5" class="text-s16 text-text ml-2">+{{ team.max_members - 5 }}</span>
          </div>
        </div>

        <button
            v-if="!isTeamMember(team)"
            class="mt-auto bg-accent !text-secondary py-2 px-4 rounded-lg font-medium text-[16px] hover:bg-accent_hover"
            @click="joinTeam(team.id)">
          Присоединиться
        </button>

        <router-link
            v-else
            :to="`/team/${team.id}`"
            class="mt-auto bg-primary !text-secondary py-2 px-4 rounded-lg font-medium text-[16px] hover:bg-primary_hover text-center block">
          На страницу команды
        </router-link>
      </div>
    </div>

    <!-- Модальное окно для создания команды -->
    <div v-if="isCreateTeamModalOpen"
         class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
      <div class="bg-fon p-8 rounded-brs w-full max-w-[500px]">
        <h2 class="text-2xl font-semibold text-text mb-4 text-center">Создание команды</h2>
        <form @submit.prevent="createTeam" class="space-y-4">
          <div>
            <label class="block text-text mb-1">Название</label>
            <input
                v-model="newTeam.name"
                type="text"
                class="w-full p-2 rounded-brs !bg-secondary focus:outline-none focus:outline-accent border-2 border-secondary"
                required
            />
          </div>
          <div>
            <label class="block text-text mb-1">Описание</label>
            <textarea
                v-model="newTeam.description"
                class="w-full p-2 rounded-brs !bg-secondary focus:outline-none focus:outline-accent border-2 border-secondary"
                required
            ></textarea>
          </div>
          <div>
            <label class="block text-text mb-1">Игра</label>
            <select
                v-model="newTeam.game"
                class="w-full p-2 rounded-brs !bg-secondary focus:outline-none focus:outline-accent border-2 border-secondary"
                required
            >
              <option v-for="game in games" :key="game.id" :value="game.id">{{ game.name }}</option>
            </select>
          </div>
          <div>
            <label class="block text-text mb-1">Тип игры</label>
            <select
                v-model="newTeam.gameType"
                class="w-full p-2 rounded-brs !bg-secondary focus:outline-none focus:outline-accent border-2 border-secondary"
                required
            >
              <option v-for="type in gameTypes" :key="type.id" :value="type.id">{{ type.name }}</option>
            </select>
          </div>
          <div class="relative">
            <label class="block text-text mb-1">Кол-во участников</label>
            <input
                type="number"
                v-model.number="newTeam.maxMembers"
                :max="hasSubscription ? null : 5"
                min="1"
                class="w-full p-2 rounded-brs !bg-secondary focus:outline-none focus:outline-accent border-2 border-secondary"
                required
                @input="validateMaxMembers"
            />
            <div v-if="!hasSubscription && newTeam.maxMembers >= 5"
                 class="absolute right-0 top-0 transform translate-x-full bg-secondary text-text p-2 rounded-lg shadow-lg text-sm w-64">
              Для создания команды с более чем 5 участниками требуется подписка
            </div>
            <p v-if="!hasSubscription" class="text-sm text-text/80 mt-1">
              Максимальное количество участников без подписки: 5
            </p>
            <p v-else class="text-sm text-accent mt-1">
              У вас есть подписка, можно создать команду с любым количеством участников
            </p>
          </div>
          <div>
            <label class="block text-text mb-1">Дата и время</label>
            <input
                type="datetime-local"
                v-model="newTeam.time"
                class="w-full p-2 rounded-brs !bg-secondary focus:outline-none focus:outline-accent border-2 border-secondary"
                required
            />
          </div>
          <div class="flex justify-between">
            <button
                type="button"
                @click="closeCreateTeamModal"
                class="p-2 bg-secondary hover:bg-secondary_hover !text-text rounded-brs transition block font-semibold"
            >
              Отменить
            </button>
            <button
                type="submit"
                class="p-2 bg-accent hover:bg-accent_hover !text-secondary rounded-brs transition block font-semibold"
                :disabled="!hasSubscription && newTeam.maxMembers > 5"
            >
              Создать
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
  <div v-else class="min-h-screen flex items-center justify-center">
    <p>Пожалуйста, войдите в систему.
      <router-link to="/login" class="text-primary hover:underline">Вход</router-link>
    </p>
  </div>
</template>

<script setup>
import {ref, computed, onMounted} from 'vue';
import {useRouter} from 'vue-router';
import {useAuthStore} from '../stores/auth';
import {useSubscriptionStore} from '../stores/subscriptionStore';
import api from '../api';

const router = useRouter();
const authStore = useAuthStore();
const subscriptionStore = useSubscriptionStore();

const teams = ref([]);
const games = ref([]);
const subscribedUserIds = ref([]);
const gameTypes = ref([]);
const searchQuery = ref('');
const selectedGame = ref('');
const selectedGameType = ref('');
const selectedDate = ref('');
const selectedPlayers = ref('');
const onlyMyTeams = ref(false);
const isCreateTeamModalOpen = ref(false);
const newTeam = ref({
  name: '',
  description: '',
  game: '',
  gameType: '',
  maxMembers: 1,
  time: '',
});

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

const isTeamMember = (team) => {
  if (!authStore.user?.id) return false;
  return team.owner_id === authStore.user.id ||
      team.members?.some(member => member.user_id === authStore.user.id);
};

onMounted(async () => {
  await authStore.checkAuth();
  if (!authStore.isAuthenticated) {
    router.push('/login');
    return;
  }
  await subscriptionStore.checkCurrentSubscription();
  await loadTeamsAndFilters();
});

const loadTeamsAndFilters = async () => {
  try {
    const [teamsRes, gamesRes, gameTypesRes, subscribedRes] = await Promise.all([
      api.get('/api/teams'),
      api.get('/api/games'),
      api.get('/api/games/types'),
      api.get('/api/subscriptions/subscribed_user_ids')
    ]);

    games.value = gamesRes.data;
    gameTypes.value = gameTypesRes.data;

    subscribedUserIds.value = subscribedRes.data;

    teams.value = teamsRes.data.map(team => ({
      ...team,
      formattedTime: formatDate(team.time),
      game: games.value.find(game => game.id === team.game_id)?.name || 'Неизвестно',
      gameType: gameTypes.value.find(type => type.id === team.game_type_id)?.name || 'Неизвестно',
      isMyTeam: team.owner_id === authStore.user?.id,
      members: team.members || [],
      ownerHasSubscription: subscribedUserIds.value.includes(team.owner_id)
    }));
  } catch (error) {
    console.error('Ошибка загрузки данных:', error);
  }
};

const filteredTeams = computed(() => {
  const filtered = teams.value.filter(team => {
    let matches = true;

    if (searchQuery.value && !team.name.toLowerCase().includes(searchQuery.value.toLowerCase()) &&
        !team.game.toLowerCase().includes(searchQuery.value.toLowerCase()) &&
        !team.gameType.toLowerCase().includes(searchQuery.value.toLowerCase())) {
      matches = false;
    }

    if (selectedGame.value && team.game_id !== selectedGame.value) {
      matches = false;
    }

    if (selectedGameType.value && team.game_type_id !== selectedGameType.value) {
      matches = false;
    }

    if (selectedDate.value) {
      const now = new Date();
      const teamDate = new Date(team.time);
      if (selectedDate.value === 'today' && teamDate.toDateString() !== now.toDateString()) {
        matches = false;
      }
      if (selectedDate.value === 'week' && (teamDate.getTime() < now.getTime() - 7 * 24 * 60 * 60 * 1000)) {
        matches = false;
      }
      if (selectedDate.value === 'month' && (teamDate.getTime() < now.getTime() - 30 * 24 * 60 * 60 * 1000)) {
        matches = false;
      }
    }

    if (selectedPlayers.value === 'small' && team.max_members > 5) {
      matches = false;
    }
    if (selectedPlayers.value === 'medium' && (team.max_members <= 5 || team.max_members > 10)) {
      matches = false;
    }
    if (selectedPlayers.value === 'large' && team.max_members <= 10) {
      matches = false;
    }

    if (onlyMyTeams.value && !team.isMyTeam) {
      matches = false;
    }

    return matches;
  });

  // Сортируем после фильтрации
  return [...filtered].sort((a, b) => {
    if (a.ownerHasSubscription && !b.ownerHasSubscription) return -1;
    if (!a.ownerHasSubscription && b.ownerHasSubscription) return 1;
    return 0;
  });
});

const openCreateTeamForm = () => {
  isCreateTeamModalOpen.value = true;
  // Сброс значений при открытии формы
  newTeam.value = {
    name: '',
    description: '',
    game: '',
    gameType: '',
    maxMembers: 1,
    time: '',
  };
};

const closeCreateTeamModal = () => {
  isCreateTeamModalOpen.value = false;
};

const validateMaxMembers = () => {
  if (!hasSubscription.value && newTeam.value.maxMembers > 5) {
    newTeam.value.maxMembers = 5;
  }
};

const createTeam = async () => {
  try {
    // Проверка ограничения на количество участников
    if (!hasSubscription.value && newTeam.value.maxMembers > 5) {
      alert('Без подписки можно создать команду только до 5 участников. Пожалуйста, оформите подписку.');
      return;
    }

    const teamData = {
      name: newTeam.value.name,
      description: newTeam.value.description,
      game_id: newTeam.value.game,
      game_type_id: newTeam.value.gameType,
      max_members: parseInt(newTeam.value.maxMembers),
      time: new Date(newTeam.value.time).toISOString(),
    };

    await api.post('/api/teams', teamData);
    await loadTeamsAndFilters();
    closeCreateTeamModal();
  } catch (error) {
    console.error('Ошибка создания команды:', error);
    if (error.response?.data?.detail) {
      alert(error.response.data.detail);
    }
  }
};

const joinTeam = async (teamId) => {
  try {
    await api.post(`/api/teams/member/${teamId}`);
    await loadTeamsAndFilters();
  } catch (error) {
    console.error('Ошибка при вступлении в команду:', error);
    if (error.response?.data?.detail) {
      alert(error.response.data.detail);
    }
  }
};
</script>