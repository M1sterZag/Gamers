<script setup>
import {useRoute} from 'vue-router'

const route = useRoute()

const siteName = 'Gamers'
const defaultTitle = 'Находите союзников для игр'
const defaultDescription = 'Находите тиммейтов, создавайте команды и общайтесь с другими геймерами'
const baseUrl = import.meta.env.VITE_BASE_URL || 'https://gamers-team.com'

const meta = {
  '/': {
    title: 'Главная',
    description: defaultDescription,
    // image: '/og-image-home.jpg'
  },
  '/teams': {
    title: 'Команды',
    description: 'Найдите или создайте команду для совместной игры',
    // image: '/og-image-teams.jpg'
  },
  '/profile': {
    title: 'Профиль',
    description: 'Ваш профиль в Gamers',
    // image: '/og-image-profile.jpg'
  },
  '/premium': {
    title: 'Премиум подписка',
    description: 'Преимущества премиум подписки Gamers+',
    // image: '/og-image-premium.jpg'
  },
  '/login': {
    title: 'Вход',
    description: 'Войдите в свой аккаунт Gamers',
    // image: '/og-image-login.jpg'
  },
  '/register': {
    title: 'Регистрация',
    description: 'Создайте новый аккаунт Gamers',
    // image: '/og-image-register.jpg'
  }
}

const currentMeta = meta[route.path] || {
  title: defaultTitle,
  description: defaultDescription,
  // image: '/og-image-default.jpg'
}
</script>

<template>
  <!-- Основные мета-теги -->
  <title>{{ currentMeta.title }} | {{ siteName }}</title>
  <meta name="description" :content="currentMeta.description">
  <meta name="keywords" content="геймеры, команды, тиммейты, игры, киберспорт">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</template>