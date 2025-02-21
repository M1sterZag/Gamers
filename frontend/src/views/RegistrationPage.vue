<template>
  <div class="min-h-screen flex items-center justify-center bg-fon">
    <div class="p-8 rounded-brs w-full max-w-sm">
      <h1 class="text-s32 font-montserrat mb-2 text-center font-semibold">Регистрация</h1>
      <form @submit.prevent="submitForm" class="space-y-4">
        <div>
          <label class="block mb-1" for="email">Email</label>
          <input
              v-model="form.email"
              type="email"
              id="email"
              class="w-full p-2 rounded-brs !bg-secondary focus:outline-none focus:outline-accent border-2 border-secondary"
          />
          <p v-if="errors.email" class="text-red-500 text-s12">{{ errors.email }}</p>
        </div>
        <div>
          <label class="block mb-1" for="username">Имя пользователя</label>
          <input
              v-model="form.username"
              type="text"
              id="username"
              class="w-full p-2 rounded-brs !bg-secondary focus:outline-none focus:outline-accent"
          />
          <p v-if="errors.username" class="text-red-500 text-s12">{{ errors.username }}</p>
        </div>
        <div>
          <label class="block mb-1" for="password">Пароль</label>
          <input
              v-model="form.password"
              type="password"
              id="password"
              class="w-full p-2 rounded-brs !bg-secondary focus:outline-none focus:outline-accent"
          />
          <p v-if="errors.password" class="text-red-500 text-s12">{{ errors.password }}</p>
        </div>
        <div>
          <label class="block mb-1" for="confirmPassword">Подтверждение пароля</label>
          <input
              v-model="form.confirmPassword"
              type="password"
              id="confirmPassword"
              class="w-full p-2 rounded-brs !bg-secondary focus:outline-none focus:outline-accent"
          />
          <p v-if="errors.confirmPassword" class="text-red-500 text-s12">{{ errors.confirmPassword }}</p>
        </div>
        <button
            type="submit"
            class="max-w-60 p-2 bg-accent hover:bg-accent_hover !text-secondary rounded-brs transition mx-auto block font-semibold"
        >
          Зарегистрироваться
        </button>
      </form>
      <div class="mt-4 text-center">
        <p>Уже есть аккаунт? <a href="/login" class="text-accent hover:underline">Вход</a></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import {reactive} from 'vue'

const form = reactive({
  email: '',
  username: '',
  password: '',
  confirmPassword: ''
})

const errors = reactive({
  email: '',
  username: '',
  password: '',
  confirmPassword: ''
})

function validateForm() {
  let valid = true

  // Очистка ошибок
  errors.email = ''
  errors.username = ''
  errors.password = ''
  errors.confirmPassword = ''

  // Проверка email
  if (!form.email) {
    errors.email = 'Email обязателен'
    valid = false
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    errors.email = 'Некорректный email'
    valid = false
  }

  // Проверка имени пользователя
  if (!form.username) {
    errors.username = 'Имя пользователя обязательно'
    valid = false
  } else if (form.username.length < 3 || form.username.length > 50) {
    errors.username = 'Имя должно быть от 3 до 50 символов'
    valid = false
  }

  // Проверка пароля
  if (!form.password) {
    errors.password = 'Пароль обязателен'
    valid = false
  } else if (form.password.length < 8 || form.password.length > 50) {
    errors.password = 'Пароль должен быть от 8 до 50 символов'
    valid = false
  }

  // Проверка подтверждения пароля
  if (form.password !== form.confirmPassword) {
    errors.confirmPassword = 'Пароли не совпадают'
    valid = false
  }

  return valid
}

function submitForm() {
  if (validateForm()) {
    console.log('Отправка данных:', {...form})
  }
}
</script>

<style scoped></style>
