<template>
  <div
      v-if="showNotice"
      class="fixed bottom-4 left-1/2 transform -translate-x-1/2 bg-secondary p-4 rounded-lg shadow-lg text-center w-full max-w-[800px]"
  >
    <p class="text-sm lg:text-16 text-text mb-3">
      Сайт использует cookie. Продолжая пользоваться этим Сайтом, вы соглашаетесь на использование файлов cookie в
      соответствии с нашими
      <a href="/static/cookie_policy.pdf" download class="text-primary underline hover:text-primary_hover">Cookie -
        Правилами</a>.
    </p>
    <button
        @click="acceptCookies"
        class="px-4 py-2 bg-accent text-secondary rounded-lg font-medium text-sm lg:text-s16 hover:bg-accent_hover transition-colors"
    >
      Хорошо
    </button>
  </div>
</template>

<script setup>
import {ref, onMounted} from 'vue';

const showNotice = ref(false);

// Проверяем, приняты ли ранее cookie
onMounted(() => {
  const hasAcceptedCookies = localStorage.getItem('cookies_accepted');
  if (!hasAcceptedCookies) {
    showNotice.value = true;
  }
});

// Функция для принятия cookie
const acceptCookies = () => {
  localStorage.setItem('cookies_accepted', 'true');
  showNotice.value = false;
};
</script>
