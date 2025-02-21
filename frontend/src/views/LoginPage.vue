<template>
  <div class="min-h-screen flex items-center justify-center bg-fon">
    <div class="p-8 rounded-brs w-full max-w-sm">
      <h1 class="text-s32 font-montserrat mb-2 text-center font-semibold">Вход</h1>
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
          <label class="block mb-1" for="password">Пароль</label>
          <input
              v-model="form.password"
              type="password"
              id="password"
              class="w-full p-2 rounded-brs !bg-secondary focus:outline-none focus:outline-accent"
          />
          <p v-if="errors.password" class="text-red-500 text-s12">{{ errors.password }}</p>
        </div>
        <button
            type="submit"
            class="w-32 p-2 bg-accent hover:bg-accent_hover !text-secondary rounded-brs transition mx-auto block font-semibold"
        >
          Войти
        </button>
      </form>
      <div class="mt-4 text-center">
        <p>Нет аккаунта? <a href="/register" class="text-accent hover:underline">Регистрация</a></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import {reactive} from 'vue'

const form = reactive({
  email: '',
  password: ''
})

const errors = reactive({
  email: '',
  password: ''
})

function validateForm() {
  let valid = true

  // Очистка ошибок
  errors.email = ''
  errors.password = ''

  // Проверка email
  if (!form.email) {
    errors.email = 'Email обязателен'
    valid = false
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    errors.email = 'Некорректный email'
    valid = false
  }

  // Проверка пароля
  if (!form.password) {
    errors.password = 'Пароль обязателен'
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
