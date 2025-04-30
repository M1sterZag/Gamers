<template>
  <!-- Мобильное меню (бургер) -->
  <button
      @click="toggleMobileMenu"
      class="wide:hidden fixed top-4 left-4 z-50 p-2 rounded-md bg-secondary text-text focus:outline-none"
      aria-label="Открыть меню"
  >
    <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-6 w-6"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
    >
      <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M4 6h16M4 12h16M4 18h16"
      />
    </svg>
  </button>
  <!-- Мобильное меню (содержимое) -->
  <transition
      enter-active-class="transition ease-out duration-200"
      enter-from-class="opacity-0 -translate-x-full"
      enter-to-class="opacity-100 translate-x-0"
      leave-active-class="transition ease-in duration-150"
      leave-from-class="opacity-100 translate-x-0"
      leave-to-class="opacity-0 -translate-x-full"
  >
    <div
        v-if="isMobileMenuOpen"
        class="fixed inset-0 z-50 bg-secondary w-64 p-6 overflow-y-auto"
    >
      <button
          @click="closeMobileMenu"
          class="absolute top-4 right-4 p-2 rounded-md text-text hover:bg-gray-700 focus:outline-none"
          aria-label="Закрыть меню"
      >
        <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
        >
          <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
          />
        </svg>
      </button>
      <router-link
          to="/"
          class="block mb-8 text-2xl font-semibold text-text hover:text-accent"
          @click="closeMobileMenu"
      >
        GAMERS
      </router-link>
      <nav class="space-y-4">
        <router-link
            v-for="(item, index) in menu"
            :key="index"
            :to="item.to"
            class="flex items-center gap-3 py-2 text-text text-base font-medium hover:text-accent"
            active-class="text-accent"
            @click="closeMobileMenu"
        >
          <component :is="item.icon" class="w-5 h-5"/>
          <span>{{ item.label }}</span>
        </router-link>
      </nav>
      <footer class="absolute bottom-6 left-6 right-6 text-center space-y-2 text-xs">
        <p>2025 © Gamers</p>
        <a href="/static/privacy_policy.pdf" download class="hover:underline block">
          Политика конфиденциальности
        </a>
        <a href="/static/terms_of_service.pdf" download class="hover:underline block">
          Пользовательское соглашение
        </a>
      </footer>
    </div>
  </transition>
</template>

<script setup>
import {ref, onMounted, onUnmounted} from 'vue';
import {useRouter} from 'vue-router';
import HomeIcon from '@/components/icons/HomeIcon.vue';
import TeamsIcon from '@/components/icons/TeamsIcon.vue';
import ProfileIcon from '@/components/icons/ProfileIcon.vue';
import PremiumIcon from '@/components/icons/PremiumIcon.vue';

const isMobileMenuOpen = ref(false);

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
};

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false;
};

const menu = [
  {label: 'Главная', to: '/', icon: HomeIcon},
  {label: 'Команды', to: '/teams', icon: TeamsIcon},
  {label: 'Профиль', to: '/profile', icon: ProfileIcon},
  {label: 'Подписки', to: '/premium', icon: PremiumIcon},
];

onMounted(() => {
  const unwatch = useRouter().afterEach(() => {
    closeMobileMenu();
  });
  onUnmounted(() => unwatch());
});
</script>