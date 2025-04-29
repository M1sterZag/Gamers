<template>
  <div class="min-h-screen flex items-center justify-center">
    <div class="p-8 bg-secondary rounded-lg w-full max-w-sm">
      <h1 class="text-s32 font-semibold text-center mb-6">Оплата подписки</h1>

      <!-- Информация о подписке -->
      <div v-if="selectedSubscription" class="mb-6">
        <p><strong>Подписка:</strong> {{ selectedSubscription.name }}</p>
        <p><strong>Цена:</strong> {{ selectedSubscription.price }} ₽</p>
        <p><strong>Длительность:</strong> {{ selectedSubscription.duration }} дней</p>
      </div>

      <form @submit.prevent="submitPayment" class="space-y-4">
        <div>
          <label for="cardNumber" class="block text-s16 font-medium">Номер карты</label>
          <input
              type="text"
              id="cardNumber"
              v-model="form.cardNumber"
              placeholder="1234 5678 9012 3456"
              class="w-full p-2 rounded-brs !bg-secondary focus:outline-none focus:outline-accent border-2 border-fon focus:border-none"
          />
          <p v-if="errors.cardNumber" class="text-red-500 text-s12">{{ errors.cardNumber }}</p>
        </div>
        <div>
          <label for="expiryDate" class="block text-s16 font-medium">Срок действия</label>
          <input
              type="text"
              id="expiryDate"
              v-model="form.expiryDate"
              placeholder="MM/YY"
              class="w-full p-2 rounded-brs !bg-secondary focus:outline-none focus:outline-accent border-2 border-fon focus:border-none"
          />
          <p v-if="errors.expiryDate" class="text-red-500 text-s12">{{ errors.expiryDate }}</p>
        </div>
        <div>
          <label for="cvv" class="block text-s16 font-medium">CVV</label>
          <input
              type="text"
              id="cvv"
              v-model="form.cvv"
              placeholder="123"
              class="w-full p-2 rounded-brs !bg-secondary focus:outline-none focus:outline-accent border-2 border-fon focus:border-none"
          />
          <p v-if="errors.cvv" class="text-red-500 text-s12">{{ errors.cvv }}</p>
        </div>
        <button
            type="submit"
            class="w-full p-2 bg-accent text-secondary rounded-lg font-medium text-s20 hover:bg-accent_hover transition"
        >
          Оплатить
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import {ref, computed, onMounted} from 'vue';
import api from '@/api';
import {useRouter} from 'vue-router';
import {useSubscriptionStore} from '@/stores/subscriptionStore';

const router = useRouter();
const subscriptionStore = useSubscriptionStore();

// Получаем ID подписки из URL
const subId = new URLSearchParams(window.location.search).get('sub_id');

// Выбранная подписка
const selectedSubscription = computed(() => {
  return subscriptionStore.getSubscriptionById(Number(subId));
});


const form = ref({
  cardNumber: '',
  expiryDate: '',
  cvv: '',
});
const errors = ref({});

// Валидация формы
const validateForm = () => {
  errors.value = {};
  let valid = true;

  if (!form.value.cardNumber.match(/^\d{16}$/)) {
    errors.value.cardNumber = 'Введите корректный номер карты (16 цифр)';
    valid = false;
  }
  if (!form.value.expiryDate.match(/^(0[1-9]|1[0-2])\/\d{2}$/)) {
    errors.value.expiryDate = 'Введите корректный срок действия (MM/YY)';
    valid = false;
  }
  if (!form.value.cvv.match(/^\d{3}$/)) {
    errors.value.cvv = 'Введите корректный CVV (3 цифры)';
    valid = false;
  }

  return valid;
};

// Отправка данных
const submitPayment = async () => {
  if (!validateForm()) return;

  try {
    await api.post(`/api/subscriptions/subscribe/${subId}`, form.value);

    // Перенаправляем обратно на страницу подписок
    router.push('/premium');
  } catch (error) {
    console.error('Ошибка при оплате:', error);
    alert('Произошла ошибка при оплате.');
  }
};

const fetchSubscriptions = async () => {
  try {
    const response = await api.get('/api/subscriptions');
    subscriptionStore.setSubscriptions(response.data);
  } catch (error) {
    console.error('Ошибка загрузки подписок:', error);
  }
};

onMounted(async () => {
  if (!subscriptionStore.subscriptions.length) {
    await fetchSubscriptions();
  }
});
</script>