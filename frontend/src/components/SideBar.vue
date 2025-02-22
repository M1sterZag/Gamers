<template>
  <aside class="p-[40px] flex flex-col items-center justify-between !bg-secondary h-screen overflow-y-auto">
    <h2 class="text-text text-s32 font-semibold">GAMERS</h2>

    <!-- Навигация -->
    <ul class="my-auto space-y-4">
      <li>
        <router-link to="/"
                     class="inline-flex items-center gap-2 py-2 text-text text-s16 font-semibold visited:text-text hover:text-accent hover:no-underline focus:no-underline focus:ring-0 focus:shadow-none ">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" class="w-[25px] h-[25px]">
            <path fill="currentColor"
                  d="m21.743 12.331l-9-10c-.379-.422-1.107-.422-1.486 0l-9 10a1 1 0 0 0-.17 1.076c.16.361.518.593.913.593h2v7a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-4h4v4a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-7h2a.998.998 0 0 0 .743-1.669"/>
          </svg>
          <span class="leading-none">Главная</span>
        </router-link>
      </li>
      <li>
        <router-link to="/teams"
                     class="inline-flex items-center gap-2 py-2 text-text text-s16 font-semibold visited:text-text hover:text-accent hover:no-underline focus:no-underline focus:ring-0 focus:shadow-none ">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" class="w-[25px] h-[25px]">
            <path fill="currentColor"
                  d="M9.5 16q-2.725 0-4.612-1.888T3 9.5t1.888-4.612T9.5 3t4.613 1.888T16 9.5q0 1.1-.35 2.075T14.7 13.3l5.6 5.6q.275.275.275.7t-.275.7t-.7.275t-.7-.275l-5.6-5.6q-.75.6-1.725.95T9.5 16m0-2q1.875 0 3.188-1.312T14 9.5t-1.312-3.187T9.5 5T6.313 6.313T5 9.5t1.313 3.188T9.5 14"/>
          </svg>
          <span class="leading-none">Команды</span>
        </router-link>
      </li>
      <li>
        <router-link to="/chats"
                     class="inline-flex items-center gap-2 py-2 text-text text-s16 font-semibold visited:text-text hover:text-accent hover:no-underline focus:no-underline focus:ring-0 focus:shadow-none ">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" class="w-[25px] h-[25px]">
            <path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                  d="M12 21.25a9.25 9.25 0 1 0-8.307-5.177c.108.22.144.468.089.706l-.816 3.536a.6.6 0 0 0 .72.72l3.535-.817a1.06 1.06 0 0 1 .706.09A9.2 9.2 0 0 0 12 21.25M7.97 9.886h8.06m-8.06 4.228h5.748"/>
          </svg>
          <span class="leading-none">Чаты</span>
        </router-link>
      </li>
      <li>
        <router-link to="/profile"
                     class="inline-flex items-center gap-2 py-2 text-text text-s16 font-semibold visited:text-text hover:text-accent hover:no-underline focus:no-underline focus:ring-0 focus:shadow-none ">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" class="w-[25px] h-[25px]">
            <path fill="currentColor" fill-rule="evenodd"
                  d="M12 4a8 8 0 0 0-6.96 11.947A4.99 4.99 0 0 1 9 14h6a4.99 4.99 0 0 1 3.96 1.947A8 8 0 0 0 12 4m7.943 14.076q.188-.245.36-.502A9.96 9.96 0 0 0 22 12c0-5.523-4.477-10-10-10S2 6.477 2 12a9.96 9.96 0 0 0 2.057 6.076l-.005.018l.355.413A9.98 9.98 0 0 0 12 22q.324 0 .644-.02a9.95 9.95 0 0 0 5.031-1.745a10 10 0 0 0 1.918-1.728l.355-.413zM12 6a3 3 0 1 0 0 6a3 3 0 0 0 0-6"
                  clip-rule="evenodd"/>
          </svg>
          <span class="leading-none">Профиль</span>
        </router-link>
      </li>
    </ul>

    <!-- Нижние ссылки -->
    <div class="mt-auto text-center space-y-2 pt-4">
      <p class="text-s12 text-text">2025 © Gamers</p>
      <router-link to="/privacy-policy"
                   class="text-text text-s12 hover:text-text visited:text-text">
        Политика конфиденциальности
      </router-link>
      <router-link to="/terms-of-service"
                   class="text-text text-s12 hover:text-text visited:text-text">
        Пользовательское соглашение
      </router-link>
    </div>
  </aside>
</template>

<script setup>
// Здесь можно добавить логику, если нужно
</script>

<style scoped>
/* Дополнительные стили для сайдбара */
</style>