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
  },
  '/teams': {
    title: 'Команды',
    description: 'Найдите или создайте команду для совместной игры',
  },
  '/profile': {
    title: 'Профиль',
    description: 'Ваш профиль в Gamers',
  },
  '/premium': {
    title: 'Премиум подписка',
    description: 'Преимущества премиум подписки Gamers+',
  },
  '/login': {
    title: 'Вход',
    description: 'Войдите в свой аккаунт Gamers',
  },
  '/register': {
    title: 'Регистрация',
    description: 'Создайте новый аккаунт Gamers',
  }
}

const currentMeta = meta[route.path] || {
  title: defaultTitle,
  description: defaultDescription,
}
</script>

<template>
  <!-- Основные мета-теги -->
  <title>{{ currentMeta.title }} | {{ siteName }}</title>
  <meta name="description" :content="currentMeta.description">
  <meta name="keywords" content="геймеры, команды, тиммейты, игры, киберспорт">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</template>