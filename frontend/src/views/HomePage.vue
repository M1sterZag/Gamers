<template>
  <div class="pt-[88px] pr-[64px] pb-[20px]">
    <div class="text-and-buttons flex justify-between items-start mb-[30px]">
      <h1 class="text-left text-[48px] font-semibold text-text">Добро пожаловать в Gamers!</h1>
      <!-- Правая часть: кнопки или профиль -->
      <div class="flex items-start gap-4">
        <template v-if="!authStore.isAuthenticated">
          <router-link to="/login">
            <button
                class="bg-accent !text-secondary py-2 px-4 rounded-lg font-medium text-[20px] hover:bg-accent_hover">
              Вход
            </button>
          </router-link>
          <router-link to="/register">
            <button
                class="bg-[#50fa7b] text-[#1b1c1e] py-2 px-4 rounded-lg font-medium text-[20px] hover:bg-accent_hover">
              Регистрация
            </button>
          </router-link>
        </template>
        <template v-else>
          <router-link
              to="/profile"
              class="flex items-center gap-2 bg-secondary rounded-lg p-2 border-2 border-secondary"
              :class="{ 'animate-neon-border': hasSubscription }"
          >
            <!-- Иконка профиля -->
            <div
                class="w-10 h-10 rounded-full overflow-hidden relative"
            >
              <img
                  v-if="authStore.user?.avatar"
                  :src="authStore.user.avatar"
                  alt="Avatar"
                  class="w-full h-full object-cover"
              />
              <div
                  v-else
                  class="w-full h-full bg-accent flex items-center justify-center text-secondary text-xl font-bold"
              >
                {{ authStore.user?.username.charAt(0).toUpperCase() }}
              </div>
            </div>

            <!-- Никнейм -->
            <span
                class="text-text font-medium text-[20px]"
            >
      {{ authStore.user?.username }}
    </span>
          </router-link>
        </template>
      </div>
    </div>

    <h2 class="text-left text-[32px] font-semibold text-text">Ищите тиммейтов, создавайте команды и общайтесь.</h2>

    <div class="cards grid grid-cols-4 gap-4 mt-[45px]">
      <!-- Карточка 1 -->
      <div class="card !bg-secondary text-text p-[20px] rounded-lg border-none flex flex-col items-start h-full">
        <p class="text-s20">Создавайте</p>
        <hr class="w-full h-[2px] bg-primary border-0 my-3">
        <div class="flex items-center gap-2 my-auto">
          <p class="text-s16">Находите тиммейтов по предпочтениям</p>
          <router-link to="/create-team">
            <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
                class="w-[40px] h-[40px] flex-shrink-0 text-accent hover:text-accent_hover cursor-pointer"
            >
              <path stroke-linecap="round" stroke-linejoin="round"
                    d="m12.75 15 3-3m0 0-3-3m3 3h-7.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"/>
            </svg>
          </router-link>
        </div>
      </div>

      <!-- Карточка 2 -->
      <div class="card !bg-secondary text-text p-[20px] rounded-lg border-none flex flex-col items-start h-full">
        <p class="text-s20">Общайтесь</p>
        <hr class="w-full h-[2px] bg-primary border-0 my-3">
        <div class="flex items-center gap-2 my-auto">
          <p class="text-s16">Общайтесь и находите друзей</p>
          <router-link to="/teams">
            <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
                class="w-[40px] h-[40px] flex-shrink-0 text-accent hover:text-accent_hover cursor-pointer"
            >
              <path stroke-linecap="round" stroke-linejoin="round"
                    d="m12.75 15 3-3m0 0-3-3m3 3h-7.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"/>
            </svg>
          </router-link>
        </div>
      </div>

      <!-- Карточка 3 -->
      <div class="card !bg-secondary text-text p-[20px] rounded-lg border-none flex flex-col items-start h-full">
        <p class="text-s20">Участвуйте</p>
        <hr class="w-full h-[2px] bg-primary border-0 my-3">
        <div class="flex items-center gap-2 my-auto">
          <p class="text-s16">Заходите в новую команду</p>
          <router-link to="/teams">
            <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
                class="w-[40px] h-[40px] flex-shrink-0 text-accent hover:text-accent_hover cursor-pointer"
            >
              <path stroke-linecap="round" stroke-linejoin="round"
                    d="m12.75 15 3-3m0 0-3-3m3 3h-7.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"/>
            </svg>
          </router-link>
        </div>
      </div>

      <!-- Карточка 4 -->
      <div class="card !bg-secondary text-text p-[20px] rounded-lg border-none flex flex-col items-start h-full">
        <p class="text-s20">Выделяйтесь</p>
        <hr class="w-full h-[2px] bg-primary border-0 my-3">
        <div class="flex items-center gap-2 my-auto">
          <p class="text-s16">Присмотритесь к премиум-подписке</p>
          <router-link to="/premium">
            <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
                class="w-[40px] h-[40px] flex-shrink-0 text-accent hover:text-accent_hover cursor-pointer"
            >
              <path stroke-linecap="round" stroke-linejoin="round"
                    d="m12.75 15 3-3m0 0-3-3m3 3h-7.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"/>
            </svg>
          </router-link>
        </div>
      </div>
    </div>

    <!-- Кнопка "Начать" с условным перенаправлением -->
    <div class="flex justify-center items-center mt-8">
      <router-link :to="authStore.isAuthenticated ? '/teams' : '/login'">
        <button
            class="bg-accent !text-secondary py-2 px-4 rounded-lg font-medium text-[20px] hover:bg-accent_hover">
          Начать
        </button>
      </router-link>
    </div>

    <!-- Остальной контент (преимущества и цены) -->
    <div class="advantages mt-[45px]">
      <div class="text-icon flex items-center gap-1">
        <h2 class="text-[32px] font-semibold text-text">Преимущества подписки Gamers+</h2>
        <svg xmlns="http://www.w3.org/2000/svg" class="w-[40px] h-[40px] text-primary" viewBox="0 0 256 256">
          <path fill="currentColor"
                d="M239.75 90.81c0 .11 0 .21-.07.32L217 195a16 16 0 0 1-15.72 13H54.71A16 16 0 0 1 39 195L16.32 91.13c0-.11-.05-.21-.07-.32A16 16 0 0 1 44 77.39l33.67 36.29l35.8-80.29a1 1 0 0 0 0-.1a16 16 0 0 1 29.06 0a1 1 0 0 0 0 .1l35.8 80.29L212 77.39a16 16 0 0 1 27.71 13.42Z"/>
        </svg>
      </div>

      <div class="cards grid grid-cols-3 mx-auto gap-10 mt-[45px]">
        <div
            class="card !bg-secondary text-text p-[20px] rounded-lg border-none flex flex-col items-stretch h-full">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
               stroke="currentColor" class="w-[40px] h-[40px] text-primary">
            <path stroke-linecap="round" stroke-linejoin="round"
                  d="M18.364 18.364A9 9 0 0 0 5.636 5.636m12.728 12.728A9 9 0 0 1 5.636 5.636m12.728 12.728L5.636 5.636"/>
          </svg>
          <p class="text-s20 mt-4 mb-2">Отключение рекламы</p>
          <p class="text-s16 mt-auto">Наслаждайтесь приложением без отвлекающей рекламы</p>
        </div>

        <div
            class="card !bg-secondary text-text p-[20px] rounded-lg border-none flex flex-col items-stretch h-full">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-[40px] h-[40px] text-primary" viewBox="0 0 16 16">
            <path fill="currentColor"
                  d="M3 2.25a.75.75 0 0 1 .75-.75h8.5a.75.75 0 0 1 0 1.5h-8.5A.75.75 0 0 1 3 2.25m5.53 2.97l3.75 3.75a.749.749 0 1 1-1.06 1.06L8.75 7.561v6.689a.75.75 0 0 1-1.5 0V7.561L4.78 10.03a.749.749 0 1 1-1.06-1.06l3.75-3.75a.75.75 0 0 1 1.06 0"/>
          </svg>
          <p class="text-s20 mt-4 mb-2">Поднятие профиля или команды в поиске</p>
          <p class="text-s16 mt-auto">Будьте на вершине списка — вас найдут первыми!</p>
        </div>

        <div
            class="card !bg-secondary text-text p-[20px] rounded-lg border-none flex flex-col items-stretch h-full">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-[40px] h-[40px] text-primary" viewBox="0 0 24 24">
            <path fill="currentColor"
                  d="M4 11q-.425 0-.712-.288T3 10V4q0-.425.288-.712T4 3h6q.425 0 .713.288T11 4v6q0 .425-.288.713T10 11zm10 0q-.425 0-.712-.288T13 10V4q0-.425.288-.712T14 3h6q.425 0 .713.288T21 4v6q0 .425-.288.713T20 11zM4 21q-.425 0-.712-.288T3 20v-6q0-.425.288-.712T4 13h6q.425 0 .713.288T11 14v6q0 .425-.288.713T10 21zm13 0q-.425 0-.712-.288T16 20v-2h-2.025q-.425 0-.7-.288T13 17t.288-.712T14 16h2v-2.025q0-.425.288-.7T17 13t.713.288T18 14v2h2.025q.425 0 .7.288T21 17t-.288.713T20 18h-2v2.025q0 .425-.288.7T17 21"/>
          </svg>
          <p class="text-s20 mt-4 mb-2">Кастомизация профиля</p>
          <p class="text-s16 mt-auto">Добавьте уникальный стиль, чтобы выделиться среди других</p>
        </div>
      </div>
    </div>

    <div class="flex justify-center items-center mt-8">
      <router-link to="/premium">
        <button
            class="bg-accent !text-secondary py-2 px-4 rounded-lg font-medium text-[20px] hover:bg-accent_hover">
          Оформить
        </button>
      </router-link>
    </div>

    <!-- Цены -->
    <div class="prices grid grid-cols-3 gap-4 justify-center mt-[45px]">
      <div class="card !bg-secondary rounded-lg p-[32px] border-secondary border-2 hover:border-accent flex flex-col">
        <h1 class="text-s32 font-medium text-text">Месяц</h1>
        <div class="flex items-baseline gap-1">
          <p class="text-s48 font-medium text-primary">300₽</p>
          <p class="text-s16 text-text opacity-80">/месяц</p>
        </div>
        <p class="text-s16 text-text mt-2">Хороший план чтобы начать пользоваться сервисом</p>
        <ul class="text-text text-s16 mt-3 flex-grow">
          <li class="flex items-center gap-1">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" class="text-primary">
              <path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                    d="m19.75 7.018l-9.257 9.257a1 1 0 0 1-1.414 0L4.25 11.446"/>
            </svg>
            <span>Преимущество 1</span>
          </li>
          <li class="flex items-center gap-1 mt-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" class="text-primary">
              <path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                    d="m19.75 7.018l-9.257 9.257a1 1 0 0 1-1.414 0L4.25 11.446"/>
            </svg>
            <span>Преимущество 2</span>
          </li>
          <li class="flex items-center gap-1 mt-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" class="text-primary">
              <path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                    d="m19.75 7.018l-9.257 9.257a1 1 0 0 1-1.414 0L4.25 11.446"/>
            </svg>
            <span>Преимущество 3</span>
          </li>
        </ul>
        <div class="mt-4 w-full">
          <router-link to="/premium">
            <button
                class="bg-accent !text-secondary py-2 px-4 rounded-lg font-medium text-[20px] hover:bg-accent_hover w-full">
              Купить
            </button>
          </router-link>
        </div>
      </div>

      <div class="card !bg-secondary rounded-lg p-[32px] border-secondary border-2 hover:border-accent flex flex-col">
        <h1 class="text-s32 font-medium text-text">3 Месяца</h1>
        <div class="flex items-baseline gap-1">
          <p class="text-s48 font-medium text-primary">300₽</p>
          <p class="text-s16 text-text opacity-80">/месяц</p>
        </div>
        <p class="text-s16 text-text mt-2">Идеальный выбор для тех, кто хочет оценить все возможности сервиса с
          выгодой!</p>
        <ul class="text-text text-s16 mt-3 flex-grow">
          <li class="flex items-center gap-1">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" class="text-primary">
              <path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                    d="m19.75 7.018l-9.257 9.257a1 1 0 0 1-1.414 0L4.25 11.446"/>
            </svg>
            <span>Преимущество 1</span>
          </li>
          <li class="flex items-center gap-1 mt-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" class="text-primary">
              <path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                    d="m19.75 7.018l-9.257 9.257a1 1 0 0 1-1.414 0L4.25 11.446"/>
            </svg>
            <span>Преимущество 2</span>
          </li>
          <li class="flex items-center gap-1 mt-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" class="text-primary">
              <path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                    d="m19.75 7.018l-9.257 9.257a1 1 0 0 1-1.414 0L4.25 11.446"/>
            </svg>
            <span>Преимущество 3</span>
          </li>
        </ul>
        <div class="mt-4 w-full">
          <router-link to="/premium">
            <button
                class="bg-accent !text-secondary py-2 px-4 rounded-lg font-medium text-[20px] hover:bg-accent_hover w-full">
              Купить
            </button>
          </router-link>
        </div>
      </div>

      <div class="card !bg-secondary rounded-lg p-[32px] border-secondary border-2 hover:border-accent flex flex-col">
        <h1 class="text-s32 font-medium text-text">Год</h1>
        <div class="flex items-baseline gap-1">
          <p class="text-s48 font-medium text-primary">300₽</p>
          <p class="text-s16 text-text opacity-80">/месяц</p>
        </div>
        <p class="text-s16 text-text mt-2">Самый выгодный план для тех, кто ценит качество и долгосрочные решения.</p>
        <ul class="text-text text-s16 mt-3 flex-grow">
          <li class="flex items-center gap-1">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" class="text-primary">
              <path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                    d="m19.75 7.018l-9.257 9.257a1 1 0 0 1-1.414 0L4.25 11.446"/>
            </svg>
            <span>Преимущество 1</span>
          </li>
          <li class="flex items-center gap-1 mt-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" class="text-primary">
              <path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                    d="m19.75 7.018l-9.257 9.257a1 1 0 0 1-1.414 0L4.25 11.446"/>
            </svg>
            <span>Преимущество 2</span>
          </li>
          <li class="flex items-center gap-1 mt-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" class="text-primary">
              <path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                    d="m19.75 7.018l-9.257 9.257a1 1 0 0 1-1.414 0L4.25 11.446"/>
            </svg>
            <span>Преимущество 3</span>
          </li>
        </ul>
        <div class="mt-4 w-full">
          <router-link to="/premium">
            <button
                class="bg-accent !text-secondary py-2 px-4 rounded-lg font-medium text-[20px] hover:bg-accent_hover w-full">
              Купить
            </button>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {computed, onMounted} from 'vue';
import {useAuthStore} from '../stores/auth';
import {useSubscriptionStore} from '../stores/subscriptionStore';

const authStore = useAuthStore();
const subscriptionStore = useSubscriptionStore();

const hasSubscription = computed(() => {
  return !!subscriptionStore.currentSubscriptionId;
});

onMounted(async () => {
  await authStore.checkAuth(); // Проверяем авторизацию при загрузке страницы
  await subscriptionStore.checkCurrentSubscription();
});
</script>
