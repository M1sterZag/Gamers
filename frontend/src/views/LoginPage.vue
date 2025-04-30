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
import {reactive} from 'vue';
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
  }

  return valid;
}

// Отправка формы
async function submitForm() {
  if (validateForm()) {
    try {
      await authStore.login(form.email, form.password);
      await router.push('/'); // Перенаправление на главную страницу
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Ошибка авторизации';
      if (errorMessage.includes('Incorrect email or password')) {
        errors.password = 'Неверный email или пароль';
      } else if (errorMessage.includes('Account is not active')) {
        errors.email = 'Аккаунт не активирован';
      } else {
        errors.password = errorMessage;
      }
    }
  }
}
</script>