<template>
  <div class="pt-[88px] pr-[64px] pl-[2px]">

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
            placeholder="Поиск команды..."
            class="w-full p-3 pl-10 text-s16 text-text rounded-lg bg-secondary focus:outline-none focus:ring-2 focus:ring-primary placeholder:text-text/50"
        />
      </div>
      <button
          class="bg-accent !text-secondary py-2 px-4 rounded-lg font-medium text-s20 hover:bg-accent_hover ml-4"
          @click="openCreateTeamForm">
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

      <label class="flex items-center text-text">
        <input type="checkbox" v-model="onlyMyTeams" class="mr-2"/>
        Мои команды
      </label>
    </div>

    <div class="teams mt-10 grid grid-cols-1 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      <div v-for="team in filteredTeams" :key="team.id"
           class="team-card bg-secondary text-text p-5 rounded-lg shadow-md flex flex-col items-center text-center">
        <h2 class="text-xl font-semibold">{{ team.name }}</h2>
        <p class="text-s16 text-text/80 mt-1">{{ team.game }}</p>
        <p class="text-s16 text-text/80 mt-1">{{ team.gameType }}</p>
        <p class="text-s16 text-text/80 mt-1">{{ team.formattedTime }}</p>
        <p class="text-s16 text-text/80 mt-2">{{ team.description }}</p>

        <!-- Отображение участников -->
        <div class="flex items-center mt-2 mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
               class="w-[27px] h-[27px] text-text">
            <path fill="currentColor" fill-rule="evenodd"
                  d="M12 4a8 8 0 0 0-6.96 11.947A4.99 4.99 0 0 1 9 14h6a4.99 4.99 0 0 1 3.96 1.947A8 8 0 0 0 12 4m7.943 14.076q.188-.245.36-.502A9.96 9.96 0 0 0 22 12c0-5.523-4.477-10-10-10S2 6.477 2 12a9.96 9.96 0 0 0 2.057 6.076l-.005.018l.355.413A9.98 9.98 0 0 0 12 22q.324 0 .644-.02a9.95 9.95 0 0 0 5.031-1.745a10 10 0 0 0 1.918-1.728l.355-.413zM12 6a3 3 0 1 0 0 6a3 3 0 0 0 0-6"
                  clip-rule="evenodd"/>
          </svg>
          <div class="flex ml-1">
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
            class="mt-auto bg-accent !text-secondary py-2 px-4 rounded-lg font-medium text-[16px] hover:bg-accent_hover">
          Присоединиться
        </button>
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

          <div>
            <label class="block text-text mb-1">Кол-во участников</label>
            <input
                type="number"
                v-model="newTeam.maxMembers"
                class="w-full p-2 rounded-brs !bg-secondary focus:outline-none focus:outline-accent border-2 border-secondary"
                required
            />
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
            >
              Создать
            </button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup>
import {ref, computed, onMounted} from 'vue';

const teams = ref([]);
const games = ref([]);
const gameTypes = ref([]);
const searchQuery = ref('');
const selectedGame = ref('');
const selectedGameType = ref('');
const selectedDate = ref('');
const selectedPlayers = ref('');
const onlyMyTeams = ref(false);
const isCreateTeamModalOpen = ref(false);  // Флаг для открытия модального окна
const newTeam = ref({
  name: '',
  description: '',
  game: '',
  gameType: '',
  maxMembers: 0,
  time: ''
});

const formatDate = (dateStr) => {
  const date = new Date(dateStr);
  return new Intl.DateTimeFormat('ru-RU', {
    day: 'numeric', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit'
  }).format(date);
};

// Загружаем команды, игры и типы игр
onMounted(async () => {
  try {
    const [teamsRes, gamesRes, gameTypesRes] = await Promise.all([
      fetch('/api/teams'),
      fetch('/api/games'),
      fetch('/api/games/types'),
    ]);

    const [teamsData, gamesData, gameTypesData] = await Promise.all([
      teamsRes.json(),
      gamesRes.json(),
      gameTypesRes.json(),
    ]);

    games.value = gamesData;
    gameTypes.value = gameTypesData;

    teams.value = teamsData.map(team => ({
      ...team,
      formattedTime: formatDate(team.time),
      game: gamesData.find(game => game.id === team.game_id)?.name || 'Неизвестно',
      gameType: gameTypesData.find(type => type.id === team.game_type_id)?.name || 'Неизвестно',
    }));

  } catch (error) {
    console.error('Ошибка загрузки данных:', error);
  }
});

const filteredTeams = computed(() => {
  return teams.value.filter(team => {
    let matches = true;

    // Фильтрация по поисковому запросу
    if (searchQuery.value && !team.name.toLowerCase().includes(searchQuery.value.toLowerCase()) &&
        !team.game.toLowerCase().includes(searchQuery.value.toLowerCase()) &&
        !team.gameType.toLowerCase().includes(searchQuery.value.toLowerCase())) {
      matches = false;
    }

    // Фильтрация по выбранной игре
    if (selectedGame.value && team.game_id !== selectedGame.value) {
      matches = false;
    }

    // Фильтрация по выбранному типу игры
    if (selectedGameType.value && team.game_type_id !== selectedGameType.value) {
      matches = false;
    }

    // Фильтрация по дате
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

    // Фильтрация по количеству игроков
    if (selectedPlayers.value === 'small' && team.max_members > 5) {
      matches = false;
    }
    if (selectedPlayers.value === 'medium' && (team.max_members <= 5 || team.max_members > 10)) {
      matches = false;
    }
    if (selectedPlayers.value === 'large' && team.max_members <= 10) {
      matches = false;
    }

    // Фильтрация по моим командам
    // if (onlyMyTeams.value && !team.isMyTeam) {
    //   matches = false;
    // }

    return matches;
  });
});

// Открытие модального окна для создания команды
const openCreateTeamForm = () => {
  isCreateTeamModalOpen.value = true;
};

// Закрытие модального окна
const closeCreateTeamModal = () => {
  isCreateTeamModalOpen.value = false;
  // Очистка данных формы
  newTeam.value = {
    name: '',
    description: '',
    game: '',
    gameType: '',
    maxMembers: 0,
    time: ''
  };
};

// Создание команды
const createTeam = () => {
  // Логика для сохранения команды (например, отправка данных на сервер)
  console.log(newTeam.value);
  closeCreateTeamModal();
};
</script>
