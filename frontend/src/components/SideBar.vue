<template>
  <aside class="p-4 lg:p-[40px] flex flex-col items-center justify-between bg-secondary h-screen overflow-y-auto">
    <router-link to="/">
      <h2 class="text-text text-xl lg:text-s32 font-semibold">GAMERS</h2>
    </router-link>

    <!-- Навигация -->
    <nav class="my-auto space-y-4">
      <ul class="space-y-2">
        <li v-for="(item, index) in menu" :key="index">
          <router-link
              :to="item.to"
              class="inline-flex items-center gap-2 py-2 px-4 text-sm lg:text-s16 font-semibold text-text hover:text-accent"
          >
            <component :is="item.icon" class="w-5 h-5 lg:w-[25px] lg:h-[25px]"/>
            <span class="leading-none">{{ item.label }}</span>
          </router-link>
        </li>
      </ul>
    </nav>

    <!-- Footer -->
    <footer class="mt-auto text-center space-y-2 pt-4 text-xs lg:text-s12">
      <p>2025 © Gamers</p>
      <a href="/static/privacy_policy.pdf" download class="block hover:underline">Политика конфиденциальности</a>
      <a href="/static/terms_of_service.pdf" download class="block hover:underline">Пользовательское соглашение</a>
    </footer>
  </aside>
</template>

<script setup>
import {defineAsyncComponent} from 'vue'

const menu = [
  {
    label: 'Главная',
    to: '/',
    icon: defineAsyncComponent(() => import('@/components/icons/HomeIcon.vue'))
  },
  {
    label: 'Команды',
    to: '/teams',
    icon: defineAsyncComponent(() => import('@/components/icons/TeamsIcon.vue'))
  },
  {
    label: 'Профиль',
    to: '/profile',
    icon: defineAsyncComponent(() => import('@/components/icons/ProfileIcon.vue'))
  },
  {
    label: 'Подписки',
    to: '/premium',
    icon: defineAsyncComponent(() => import('@/components/icons/PremiumIcon.vue'))
  }
]
</script>