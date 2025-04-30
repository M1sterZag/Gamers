<template>
  <main class="">
    <!-- Заголовок -->
    <h1 class="text-3xl lg:text-5xl font-semibold text-text leading-tight mb-8">
      Преимущества подписки Gamers+
    </h1>

    <!-- Преимущества -->
    <section class="grid grid-cols-1 sm:grid-cols-2 gap-4 lg:gap-6 mb-5">
      <div
          v-for="(benefit, index) in benefits"
          :key="index"
          class="bg-secondary p-4 lg:p-6 rounded-lg flex flex-col items-center text-center transition-transform hover:scale-105"
      >
        <div class="mb-4">
          <div v-html="benefit.icon" class="w-8 h-8 lg:w-12 lg:h-12 mx-auto"></div>
        </div>
        <h3 class="text-lg lg:text-xl font-bold mb-2">{{ benefit.title }}</h3>
        <p class="text-sm lg:text-base text-text/80">{{ benefit.description }}</p>
      </div>
    </section>

    <!-- Список доступных подписок -->
    <h2 class="text-2xl lg:text-4xl font-semibold text-text mb-6">Выберите тариф</h2>
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 lg:gap-6">
      <div
          v-for="subscription in subscriptions"
          :key="subscription.id"
          class="bg-secondary p-4 lg:p-6 rounded-lg flex flex-col justify-between h-full"
      >
        <div>
          <h3 class="text-lg lg:text-xl font-bold mb-4">{{ subscription.name }}</h3>
          <p><strong>Срок действия:</strong> {{ subscription.duration }} дней</p>
          <p><strong>Цена:</strong> {{ subscription.price }} ₽</p>
        </div>
        <div class="mt-4">
          <button
              v-if="currentSubscription?.subscription_id !== subscription.id"
              class="w-full bg-accent text-secondary py-2 px-4 rounded-lg font-medium text-sm lg:text-base hover:bg-accent_hover transition-colors"
              @click="purchaseSubscription(subscription.id)"
          >
            Оформить подписку
          </button>
          <p v-else class="text-accent text-sm lg:text-base">У вас есть данная подписка</p>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import {ref, onMounted} from 'vue';
import api from '@/api';
import {useSubscriptionStore} from '@/stores/subscriptionStore';

const subscriptionStore = useSubscriptionStore();
const subscriptions = ref([]);
const currentSubscription = ref(null);

// Преимущества подписки с новыми SVG-иконками
const benefits = ref([
  {
    title: "Больше союзников",
    description: "Создавайте команды с более чем 5 участниками.",
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 28 28"><path fill="currentColor" d="M17.754 11c.966 0 1.75.784 1.75 1.75v6.749a5.501 5.501 0 0 1-11.002 0V12.75c0-.966.783-1.75 1.75-1.75zM3.75 11l4.382-.002a2.73 2.73 0 0 0-.621 1.532l-.01.22v6.749c0 1.133.291 2.199.8 3.127A4.5 4.5 0 0 1 2 18.499V12.75A1.75 1.75 0 0 1 3.751 11m16.124-.002L24.25 11c.966 0 1.75.784 1.75 1.75v5.75a4.5 4.5 0 0 1-6.298 4.127l.056-.102c.429-.813.69-1.729.738-2.7l.008-.326V12.75c0-.666-.237-1.276-.63-1.752M14 3a3.5 3.5 0 1 1 0 7a3.5 3.5 0 0 1 0-7m8.003 1a3 3 0 1 1 0 6a3 3 0 0 1 0-6M5.997 4a3 3 0 1 1 0 6a3 3 0 0 1 0-6"/></svg>`,
  },
  {
    title: "Поднятие команды в поиске",
    description: "Команды выше в списке поиска.",
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 48 48"><g fill="none" stroke="currentColor" stroke-linejoin="round" stroke-width="4"><path d="M21 38c9.389 0 17-7.611 17-17S30.389 4 21 4S4 11.611 4 21s7.611 17 17 17Z"/><path stroke-linecap="round" d="M26.657 14.343A7.98 7.98 0 0 0 21 12a7.98 7.98 0 0 0-5.657 2.343m17.879 18.879l8.485 8.485"/></g></svg>`,
  },
  {
    title: "Статистика в профиле",
    description: "Отображение последних команд в профиле.",
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"><path stroke-miterlimit="5.759" d="M3 3v16a2 2 0 0 0 2 2h16"/><path stroke-miterlimit="5.759" d="m7 14l4-4l4 4l6-6"/><path d="M18 8h3v3"/></g></svg>`,
  },
  {
    title: "Выделение никнейма и команды",
    description: "Анимированная граница вокруг профиля и команды.",
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24"><path fill="currentColor" d="M2 4a2 2 0 0 1 2-2h3v2H4v3H2zm20 4v3h-2V4h-3V2h3a2 2 0 0 1 2 2m-2 16v-3h2v3a2 2 0 0 1-2 2h-3v-2zM2 20v-3h2v3h3v2H4a2 2 0 0 1-2-2m8-18h4v2h-4zm0 18h4v2h-4zm10-10h2v4h-2zM2 10h2v4H2z"/></svg>`,
  },
]);

// Загрузка доступных подписок
const fetchSubscriptions = async () => {
  try {
    const response = await api.get('/api/subscriptions');
    subscriptions.value = response.data;
    subscriptionStore.setSubscriptions(response.data);
  } catch (error) {
    console.error('Ошибка загрузки подписок:', error);
  }
};

// Проверка текущей подписки пользователя
const checkCurrentSubscription = async () => {
  try {
    const response = await api.get('/api/subscriptions/check_subscription');
    currentSubscription.value = response.data;
  } catch (error) {
    if (error.response?.status === 403) {
      currentSubscription.value = null; // Нет активной подписки
    } else {
      console.error('Ошибка проверки подписки:', error);
    }
  }
};

// Оформление подписки
const purchaseSubscription = async (subId) => {
  try {
    // Проверяем, есть ли уже активная подписка
    if (currentSubscription.value && currentSubscription.value.subscription_id === subId) {
      alert('У вас уже оформлена эта подписка.');
      return;
    }

    // Если есть любая активная подписка, запрещаем оформление новой
    if (currentSubscription.value) {
      alert('У вас уже есть активная подписка. Вы можете продлить её позже.');
      return;
    }

    // Если нет активной подписки, перенаправляем на страницу оплаты
    subscriptionStore.setCurrentSubscriptionId(subId);
    window.location.href = `/payment?sub_id=${subId}`;
  } catch (error) {
    console.error('Ошибка оформления подписки:', error);
    alert('Произошла ошибка при оформлении подписки.');
  }
};

// Загрузка данных при монтировании компонента
onMounted(async () => {
  await fetchSubscriptions();
  await checkCurrentSubscription();
});
</script>