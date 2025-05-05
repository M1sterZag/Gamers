<template>
  <transition name="fade">
    <div
        v-if="isVisible"
        class="fixed bottom-4 left-1/2 transform -translate-x-1/2 w-full max-w-[400px] sm:max-w-[500px] p-4 rounded-lg shadow-lg flex items-center justify-between bg-secondary"
        :class="notificationClass"
    >
      <!-- Иконка -->
      <div class="mr-3">
        <svg
            v-if="type === 'success'"
            xmlns="http://www.w3.org/2000/svg"
            class="w-6 h-6"
            :class="iconClass"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
        >
          <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
          <polyline points="22 4 12 14.01 9 11.01"></polyline>
        </svg>
        <svg
            v-else-if="type === 'error'"
            xmlns="http://www.w3.org/2000/svg"
            class="w-6 h-6"
            :class="iconClass"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
        >
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="8" x2="12" y2="12"></line>
          <line x1="12" y1="16" x2="12.01" y2="16"></line>
        </svg>
      </div>

      <!-- Текст -->
      <p class="flex-1 text-sm sm:text-base" :class="textClass">{{ message }}</p>

      <!-- Кнопка закрытия -->
      <button
          @click="closeNotification"
          class="ml-3 p-1 rounded-full hover:bg-opacity-20 transition-colors"
          :class="closeButtonClass"
          aria-label="Закрыть уведомление"
      >
        <svg
            xmlns="http://www.w3.org/2000/svg"
            class="w-4 h-4"
            :class="closeIconClass"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
        >
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
    </div>
  </transition>
</template>

<script setup>
import {computed, ref} from 'vue';

// Пропсы для настройки уведомления
const props = defineProps({
  type: {
    type: String,
    default: 'success', // 'success' или 'error'
  },
  message: {
    type: String,
    required: true,
  },
  duration: {
    type: Number,
    default: 3000, // Время отображения в миллисекундах
  },
});

// Состояние видимости уведомления
const isVisible = ref(true);

// Закрытие уведомления
const closeNotification = () => {
  isVisible.value = false;
};

// Автоматическое закрытие через duration
setTimeout(() => {
  closeNotification();
}, props.duration);

// Динамические классы для цветов текста, иконок и кнопки закрытия
const notificationClass = computed(() => {
  return {
    'text-accent': props.type === 'success',
    'text-red-500': props.type === 'error',
  };
});

const iconClass = computed(() => {
  return {
    'text-accent': props.type === 'success',
    'text-red-500': props.type === 'error',
  };
});

const textClass = computed(() => {
  return {
    'text-accent': props.type === 'success',
    'text-red-500': props.type === 'error',
  };
});

const closeButtonClass = computed(() => {
  return {
    'hover:bg-accent/20': props.type === 'success',
    'hover:bg-red-500/20': props.type === 'error',
  };
});

const closeIconClass = computed(() => {
  return {
    'text-accent': props.type === 'success',
    'text-red-500': props.type === 'error',
  };
});
</script>

<style scoped>
/* Анимация появления и исчезновения */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
</style>