<template>
  <main class="min-h-screen flex items-center justify-center bg-fon">
    <!-- Семантический контейнер -->
    <section class="p-6 sm:p-8 rounded-lg w-full max-w-sm bg-background">
      <h1 class="text-s32 font-montserrat text-center font-semibold text-text mb-6">Вход</h1>

      <!-- Форма входа -->
      <form @submit.prevent="submitForm" class="space-y-4">
        <!-- Поле Email -->
        <div>
          <label for="email" class="block mb-1 text-s16 font-medium text-text">Email</label>
          <input
              v-model="form.email"
              type="email"
              id="email"
              placeholder="Введите email"
              class="w-full p-3 rounded-lg bg-secondary focus:outline-none focus:border-accent border-2 border-secondary transition"
          />
          <p v-if="errors.email" class="text-red-500 text-s12 mt-1">{{ errors.email }}</p>
        </div>

        <!-- Поле Пароль -->
        <div>
          <label for="password" class="block mb-1 text-s16 font-medium text-text">Пароль</label>
          <input
              v-model="form.password"
              type="password"
              id="password"
              placeholder="Введите пароль"
              class="w-full p-3 rounded-lg bg-secondary focus:outline-none focus:border-accent border-2 border-secondary transition"
          />
          <p v-if="errors.password" class="text-red-500 text-s12 mt-1">{{ errors.password }}</p>
        </div>

        <!-- Кнопка Войти -->
        <button
            type="submit"
            class="w-full py-3 bg-accent hover:bg-accent_hover text-secondary rounded-lg font-semibold text-s16 transition"
        >
          Войти
        </button>
      </form>

      <div class="mt-4 text-center">
        <a
            :href="oauthUrl"
            class="
            inline-flex items-center justify-center
            w-full py-3

            bg-stone-50
            hover:bg-stone-200
            /* обводка и hover */
            border
            border-stone-50
            hover:border-stone-200

            rounded-[8px]

            font-medium text-s16 text-secondary
            transition
            "
        >
          <!-- иконка Яндекса -->
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" class="w-5 h-5 mr-2">
            <path fill="#d61e3b"
                  d="M21.88 2h-4c-4 0-8.07 3-8.07 9.62a8.33 8.33 0 0 0 4.14 7.66L9 28.13a1.25 1.25 0 0 0 0 1.27a1.21 1.21 0 0 0 1 .6h2.49a1.24 1.24 0 0 0 1.2-.75l4.59-9h.34v8.62a1.14 1.14 0 0 0 1.2 1.13H22a1.12 1.12 0 0 0 1.16-1.06V3.22A1.19 1.19 0 0 0 22 2ZM18.7 16.28h-.59c-2.3 0-3.66-1.87-3.66-5c0-3.9 1.73-5.29 3.34-5.29h.94Z"/>
          </svg>
          Войти через Яндекс
        </a>
      </div>

      <!-- Ссылка на регистрацию -->
      <div class="mt-6 text-center">
        <p class="text-s14 text-text/80">
          Нет аккаунта?
          <router-link to="/register" class="text-primary hover:underline visited:text-primary font-medium">
            Регистрация
          </router-link>
        </p>
      </div>
    </section>
  </main>
</template>

<script setup>
import {computed, onMounted, reactive} from 'vue';
import {useRouter} from 'vue-router';
import {useAuthStore} from '../stores/auth';

const router = useRouter();
const authStore = useAuthStore();

// Реактивная форма
const form = reactive({
  email: '',
  password: '',
});

// Ошибки валидации
const errors = reactive({
  email: '',
  password: '',
});

const clientId = 'e0bc580e804241e5ba995640c9acd8d2';
const redirectUri = encodeURIComponent('https://gamers-team.ru/api/oauth/yandex/callback');
const oauthUrl = computed(() =>
    `https://oauth.yandex.ru/authorize?response_type=code&client_id=${clientId}&redirect_uri=${redirectUri}`
);

// Валидация формы
function validateForm() {
  let valid = true;
  errors.email = '';
  errors.password = '';

  if (!form.email) {
    errors.email = 'Email обязателен';
    valid = false;
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    errors.email = 'Некорректный email';
    valid = false;
  }

  if (!form.password) {
    errors.password = 'Пароль обязателен';
    valid = false;
  } else if (form.password.length < 8) {
    errors.password = 'Пароль должен содержать минимум 8 символов';
    valid = false;
  }

  return valid;
}

// Отправка формы
async function submitForm() {
  if (!validateForm()) return;

  try {
    await authStore.login(form.email, form.password);
    await router.push('/'); // Перенаправление на главную страницу
  } catch (error) {
    console.error('Ошибка авторизации:', error);

    // Очистка предыдущих ошибок
    errors.email = '';
    errors.password = '';

    const errorData = error.response?.data;

    if (Array.isArray(errorData)) {
      // Обработка ошибок валидации с сервера
      errorData.forEach((err) => {
        if (err.loc.includes('email')) {
          errors.email = err.msg || 'Некорректный email';
        } else if (err.loc.includes('password')) {
          errors.password = err.msg || 'Некорректный пароль';
        }
      });
    } else if (errorData?.detail) {
      // Обработка других ошибок
      if (errorData.detail.includes('Incorrect email or password')) {
        errors.password = 'Неверный email или пароль';
      } else if (errorData.detail.includes('Account is not active')) {
        errors.email = 'Аккаунт не активирован';
      } else {
        errors.password = errorData.detail || 'Произошла ошибка авторизации';
      }
    } else {
      errors.password = 'Неизвестная ошибка авторизации';
    }
  }
}
</script>