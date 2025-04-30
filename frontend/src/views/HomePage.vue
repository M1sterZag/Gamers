<template>
  <main class="">
    <header>
      <div class="flex flex-col lg:flex-row justify-between xs:items-center items-start gap-3 mb-4 lg:mb-[30px]">
        <h1 class="text-2xl lg:text-4xl font-semibold text-text leading-tight">
          Добро пожаловать в Gamers!
        </h1>
        <nav class="flex gap-3 lg:w-auto">
          <template v-if="!authStore.isAuthenticated">
            <router-link to="/login" class="w-full sm:w-auto flex-1 sm:flex-none">
              <button
                  class="w-full bg-accent text-secondary py-2 px-4 rounded-lg font-medium text-base lg:text-xl hover:bg-accent_hover transition-colors"
              >
                Вход
              </button>
            </router-link>
            <router-link to="/register" class="w-full sm:w-auto flex-1 sm:flex-none">
              <button
                  class="w-full  bg-[#50fa7b] text-[#1b1c1e] py-2 px-4 rounded-lg font-medium text-base lg:text-xl hover:bg-[#45e06d] transition-colors"
              >
                Регистрация
              </button>
            </router-link>
          </template>
          <template v-else>
            <router-link
                to="/profile"
                class="flex items-center gap-2 bg-secondary rounded-lg p-2 border-2 border-secondary w-full sm:w-auto"
                :class="{ 'animate-neon-border': hasSubscription }"
            >
              <div class="w-8 h-8 lg:w-10 lg:h-10 rounded-full overflow-hidden relative bg-gray-700">
                <img
                    v-if="authStore.user?.avatar"
                    :src="authStore.user.avatar"
                    alt="Avatar"
                    class="w-full h-full object-cover"
                />
                <div
                    v-else
                    class="w-full h-full bg-accent flex items-center justify-center text-secondary text-lg lg:text-xl font-bold"
                >
                  {{ authStore.user?.username?.charAt(0).toUpperCase() || 'U' }}
                </div>
              </div>
              <span class="font-medium text-base lg:text-xl text-text whitespace-nowrap">
                {{ authStore.user?.username || 'Профиль' }}
              </span>
            </router-link>
          </template>
        </nav>
      </div>
    </header>

    <section>
      <h2 class="text-2xl lg:text-4xl font-semibold text-text mb-6 lg:mb-8">
        Ищите тиммейтов, создавайте команды и общайтесь.
      </h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6 mt-6 lg:mt-[45px]">
        <router-link
            v-for="(card, index) in cards"
            :key="index"
            :to="card.to"
            class="bg-secondary text-text p-4 lg:p-6 rounded-lg border-2 border-transparent hover:border-accent transition-colors flex flex-col h-full"
        >
          <p class="text-lg lg:text-xl font-medium">{{ card.title }}</p>
          <hr class="w-full h-[2px] bg-primary border-0 my-3 lg:my-4">
          <div class="flex items-center justify-between mt-auto">
            <p class="text-sm lg:text-base flex-1">{{ card.description }}</p>
            <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
                class="w-6 h-6 lg:w-8 lg:h-8 flex-shrink-0 text-accent ml-2"
            >
              <path stroke-linecap="round" stroke-linejoin="round"
                    d="m12.75 15 3-3m0 0-3-3m3 3h-7.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"/>
            </svg>
          </div>
        </router-link>
      </div>
    </section>

    <section class="mt-12 lg:mt-[45px]">
      <header class="flex items-center gap-2 lg:gap-3 mb-6 lg:mb-8">
        <h2 class="text-2xl lg:text-4xl font-semibold text-text">
          Преимущества подписки Gamers+
        </h2>
        <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 256 256"
            class="w-10 h-10 text-primary"
        >
          <path
              fill="currentColor"
              d="M239.75 90.81c0 .11 0 .21-.07.32L217 195a16 16 0 0 1-15.72 13H54.71A16 16 0 0 1 39 195L16.32 91.13c0-.11-.05-.21-.07-.32A16 16 0 0 1 44 77.39l33.67 36.29l35.8-80.29a1 1 0 0 0 0-.1a16 16 0 0 1 29.06 0a1 1 0 0 0 0 .1l35.8 80.29L212 77.39a16 16 0 0 1 27.71 13.42Z"
          />
        </svg>
      </header>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 lg:gap-6">
        <div
            v-for="(benefit, index) in benefits"
            :key="index"
            class="bg-secondary text-text p-4 lg:p-6 rounded-lg flex flex-col h-full"
        >
          <component :is="benefit.icon" class="w-8 h-8 lg:w-10 lg:h-10 text-primary"/>
          <p class="text-lg lg:text-xl font-medium mt-4 mb-2">{{ benefit.title }}</p>
          <p class="text-sm lg:text-base text-text/80">{{ benefit.description }}</p>
        </div>
      </div>
      <div class="flex justify-center items-center mt-8 lg:mt-10">
        <router-link to="/premium" class="w-full sm:w-auto">
          <button
              class="w-full bg-accent text-secondary py-2 px-6 rounded-lg font-medium text-lg lg:text-xl hover:bg-accent_hover transition-colors"
          >
            Оформить
          </button>
        </router-link>
      </div>
    </section>
  </main>
</template>

<script setup>
import {computed, onMounted} from 'vue';
import {useAuthStore} from '../stores/auth';
import {useSubscriptionStore} from '../stores/subscriptionStore';
import MoreAlliesIcon from '@/components/icons/MoreAlliesIcon.vue';
import TeamBoostIcon from '@/components/icons/TeamBoostIcon.vue';
import UsernameStyleIcon from '@/components/icons/UsernameStyleIcon.vue';

const authStore = useAuthStore();
const subscriptionStore = useSubscriptionStore();

const hasSubscription = computed(() => !!subscriptionStore.currentSubscriptionId);

const cards = [
  {title: 'Создавайте', description: 'Находите тиммейтов по предпочтениям', to: '/create-team'},
  {title: 'Общайтесь', description: 'Общайтесь и находите друзей', to: '/teams'},
  {title: 'Участвуйте', description: 'Заходите в новую команду', to: '/teams'},
  {title: 'Выделяйтесь', description: 'Присмотритесь к премиум-подписке', to: '/premium'},
];

const benefits = [
  {
    title: 'Больше союзников',
    description: 'Создавайте команды с более чем 5 участниками',
    icon: MoreAlliesIcon,
  },
  {
    title: 'Поднятие команды в поиске',
    description: 'Будьте на вершине списка — вас найдут первыми!',
    icon: TeamBoostIcon,
  },
  {
    title: 'Выделение никнейма и команды',
    description: 'Получите уникальный стиль, чтобы выделиться среди других',
    icon: UsernameStyleIcon,
  },
];

onMounted(async () => {
  await authStore.checkAuth();
  await subscriptionStore.checkCurrentSubscription();
});
</script>