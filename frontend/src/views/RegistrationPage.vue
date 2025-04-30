<template>
  <main class="min-h-screen flex items-center justify-center bg-fon">
    <!-- Семантический контейнер -->
    <section class="p-6 sm:p-8 rounded-lg w-full max-w-sm bg-background">
      <h1 class="text-s32 font-montserrat text-center font-semibold text-text mb-6">Регистрация</h1>

      <!-- Форма регистрации -->
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

        <!-- Поле Имя пользователя -->
        <div>
          <label for="username" class="block mb-1 text-s16 font-medium text-text">Имя пользователя</label>
          <input
              v-model="form.username"
              type="text"
              id="username"
              placeholder="Введите имя пользователя"
              class="w-full p-3 rounded-lg bg-secondary focus:outline-none focus:border-accent border-2 border-secondary transition"
          />
          <p v-if="errors.username" class="text-red-500 text-s12 mt-1">{{ errors.username }}</p>
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

        <!-- Поле Подтверждение пароля -->
        <div>
          <label for="confirmPassword" class="block mb-1 text-s16 font-medium text-text">Подтверждение пароля</label>
          <input
              v-model="form.confirmPassword"
              type="password"
              id="confirmPassword"
              placeholder="Подтвердите пароль"
              class="w-full p-3 rounded-lg bg-secondary focus:outline-none focus:border-accent border-2 border-secondary transition"
          />
          <p v-if="errors.confirmPassword" class="text-red-500 text-s12 mt-1">{{ errors.confirmPassword }}</p>
        </div>

        <!-- Чекбокс -->
        <div class="flex items-center space-x-2">
          <input
              v-model="acceptTerms"
              type="checkbox"
              class="rounded border-accent text-accent focus:ring-accent"
              required
          />
          <label class="text-s12 text-text/80">
            Я принимаю
            <a href="/static/privacy_policy.pdf" download class="text-primary underline hover:text-primary_hover">
              политику конфиденциальности
            </a>
            и
            <a href="/static/terms_of_service.pdf" download class="text-primary underline hover:text-primary_hover">
              пользовательское соглашение
            </a>.
          </label>
        </div>

        <!-- Кнопка Зарегистрироваться -->
        <button
            type="submit"
            class="w-full py-3 bg-accent hover:bg-accent_hover text-secondary rounded-lg font-semibold text-s16 transition"
        >
          Зарегистрироваться
        </button>
      </form>

      <!-- Ссылка на вход -->
      <div class="mt-6 text-center">
        <p class="text-s14 text-text/80">
          Уже есть аккаунт?
          <router-link to="/login" class="text-primary hover:underline visited:text-primary font-medium">
            Вход
          </router-link>
        </p>
      </div>
    </section>
  </main>
</template>

<script setup>
import {reactive, ref} from 'vue';
import {useRouter} from 'vue-router';
import {useAuthStore} from '../stores/auth';

const router = useRouter();
const authStore = useAuthStore();

// Реактивная форма
const form = reactive({
  email: '',
  username: '',
  password: '',
  confirmPassword: '',
});

// Состояние чекбокса
const acceptTerms = ref(false);

// Ошибки валидации
const errors = reactive({
  email: '',
  username: '',
  password: '',
  confirmPassword: '',
});

// Валидация формы
function validateForm() {
  let valid = true;
  errors.email = '';
  errors.username = '';
  errors.password = '';
  errors.confirmPassword = '';

  if (!form.email) {
    errors.email = 'Email обязателен';
    valid = false;
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    errors.email = 'Некорректный email';
    valid = false;
  }

  if (!form.username) {
    errors.username = 'Имя пользователя обязательно';
    valid = false;
  } else if (form.username.length < 3 || form.username.length > 50) {
    errors.username = 'Имя должно быть от 3 до 50 символов';
    valid = false;
  }

  if (!form.password) {
    errors.password = 'Пароль обязателен';
    valid = false;
  } else if (form.password.length < 8 || form.password.length > 50) {
    errors.password = 'Пароль должен быть от 8 до 50 символов';
    valid = false;
  }

  if (form.password !== form.confirmPassword) {
    errors.confirmPassword = 'Пароли не совпадают';
    valid = false;
  }

  if (!acceptTerms.value) {
    alert('Вы должны принять политику конфиденциальности и пользовательское соглашение.');
    valid = false;
  }

  return valid;
}

// Отправка формы
async function submitForm() {
  if (validateForm()) {
    try {
      await authStore.register(form.email, form.username, form.password, form.confirmPassword);
      await router.push('/login');
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Ошибка регистрации';
      if (errorMessage.includes('User already exists')) {
        errors.email = 'Пользователь с таким email уже существует';
      } else if (error.response?.status === 422) {
        errors.confirmPassword = 'Ошибка в данных. Проверьте все поля';
      } else {
        errors.email = errorMessage;
      }
    }
  }
}
</script>