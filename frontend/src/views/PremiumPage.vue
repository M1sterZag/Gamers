<template>
  <div class="pt-[88px] pr-[64px] pl-[2px]">
    <!-- Заголовок -->
    <h1 class="text-left text-[48px] font-semibold text-text">Подписки</h1>

    <!-- Информация о текущей подписке -->
    <div v-if="currentSubscription" class="bg-secondary p-6 rounded-lg mb-6">
      <h2 class="text-s24 font-bold mb-4">Ваша текущая подписка:</h2>
      <p><strong>Тип:</strong> {{ currentSubscription.name }}</p>
      <p><strong>Активна до:</strong> {{ formatDate(currentSubscription.end_date) }}</p>
    </div>
    <div v-else class="bg-secondary p-6 rounded-lg mb-6">
      <p class="text-s20">У вас нет активной подписки.</p>
    </div>

    <!-- Список доступных подписок -->
    <div>
      <h2 class="text-s32 font-bold mb-6">Доступные подписки</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="subscription in subscriptions" :key="subscription.id" class="bg-secondary p-6 rounded-lg">
          <h3 class="text-s24 font-bold mb-4">{{ subscription.name }}</h3>
          <p><strong>Срок действия:</strong> {{ subscription.duration }} дней</p>
          <p><strong>Цена:</strong> {{ subscription.price }} ₽</p>
          <button
              class="mt-4 bg-accent !text-secondary py-2 px-4 rounded-lg font-medium text-s20 hover:bg-accent_hover transition"
              @click="purchaseSubscription(subscription.id)"
          >
            Оформить подписку
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, onMounted} from 'vue';
import api from '@/api';

const subscriptions = ref([]);
const currentSubscription = ref(null);

// Функция для форматирования даты
const formatDate = (dateStr) => {
  const date = new Date(dateStr);
  return new Intl.DateTimeFormat('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  }).format(date);
};

// Загрузка доступных подписок
const fetchSubscriptions = async () => {
  try {
    const response = await api.get('/api/subscriptions');
    subscriptions.value = response.data;
  } catch (error) {
    console.error('Ошибка загрузки подписок:', error);
  }
};

// Проверка текущей подписки пользователя
const checkCurrentSubscription = async () => {
  try {
    const response = await api.post('/api/subscriptions/check_subscription');
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
    await api.post(`/api/subscribe/${subId}`);
    await checkCurrentSubscription(); // Обновляем информацию о текущей подписке
    alert('Подписка успешно оформлена!');
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

<style scoped></style>