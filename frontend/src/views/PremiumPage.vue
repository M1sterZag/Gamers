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
        <div class="mb-2">
          <component :is="benefit.icon" class="w-8 h-8 lg:w-12 lg:h-12 text-primary"/>
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
import {onMounted, ref} from 'vue';
import api from '@/api';
import {useSubscriptionStore} from '@/stores/subscriptionStore';
import {useNotificationStore} from '@/stores/notificationStore';
import MoreAlliesIcon from "@/components/icons/MoreAlliesIcon.vue";
import UsernameStyleIcon from "@/components/icons/UsernameStyleIcon.vue";
import ProfileStatisticIcon from "@/components/icons/ProfileStatisticIcon.vue";
import TeamBoostIcon from "@/components/icons/TeamBoostIcon.vue";

const subscriptionStore = useSubscriptionStore();
const notificationStore = useNotificationStore();

const subscriptions = ref([]);
const currentSubscription = ref(null);

// Преимущества подписки с новыми SVG-иконками
const benefits = [
  {
    title: "Больше союзников",
    description: "Создавайте команды с более чем 5 участниками.",
    icon: MoreAlliesIcon,
  },
  {
    title: "Поднятие команды в поиске",
    description: "Команды выше в списке поиска.",
    icon: TeamBoostIcon
  },
  {
    title: "Статистика в профиле",
    description: "Отображение последних команд в профиле.",
    icon: ProfileStatisticIcon
  },
  {
    title: "Выделение никнейма и команды",
    description: "Анимированная граница вокруг профиля и команды.",
    icon: UsernameStyleIcon
  },
];

// Загрузка доступных подписок
const fetchSubscriptions = async () => {
  try {
    const response = await api.get('/api/subscriptions');
    subscriptions.value = response.data;
    subscriptionStore.setSubscriptions(response.data);
  } catch (error) {
    console.error('Ошибка загрузки подписок:', error);
    notificationStore.showNotification('error', 'Не удалось загрузить данные о подписках.');
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
    }
  }
};

// Оформление подписки
const purchaseSubscription = async (subId) => {
  try {
    // Проверяем, есть ли уже активная подписка
    if (currentSubscription.value && currentSubscription.value.subscription_id === subId) {
      notificationStore.showNotification('info', 'У вас уже оформлена эта подписка.');
      return;
    }

    // Если есть любая активная подписка, запрещаем оформление новой
    if (currentSubscription.value) {
      notificationStore.showNotification('warning', 'У вас уже есть активная подписка. Вы можете продлить её позже.');
      return;
    }

    // Создаем платеж
    const response = await api.post(`/api/subscriptions/create_payment/${subId}`);
    // Перенаправляем пользователя на страницу оплаты
    window.location.href = response.data.confirmation_url;
  } catch (error) {
    console.error('Ошибка оформления подписки:', error);
    notificationStore.showNotification('error', 'Произошла ошибка при оформлении подписки.');
  }
};

// Загрузка данных при монтировании компонента
onMounted(async () => {
  await fetchSubscriptions();
  await checkCurrentSubscription();
});
</script>