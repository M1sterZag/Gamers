<template>
  <main class="">
    <!-- Заголовок -->
    <h1 class="text-3xl font-semibold text-text text-center mb-3">
      Оплата подписки
    </h1>

    <!-- Информация о подписке -->
    <section class="mb-5">
      <div v-if="selectedSubscription" class="bg-secondary p-4 lg:p-6 rounded-lg shadow-md max-w-sm mx-auto">
        <p><strong>Подписка:</strong> {{ selectedSubscription.name }}</p>
        <p><strong>Цена:</strong> {{ selectedSubscription.price }} ₽</p>
        <p><strong>Длительность:</strong> {{ selectedSubscription.duration }} дней</p>
      </div>
      <p v-else class="text-center text-text/80">Выберите подписку для продолжения.</p>
    </section>

    <!-- Форма оплаты -->
    <form @submit.prevent="submitPayment" class="max-w-sm mx-auto space-y-4">
      <div>
        <label for="cardNumber" class="block text-sm lg:text-base font-medium text-text">Номер карты</label>
        <input
            type="text"
            id="cardNumber"
            v-model="form.cardNumber"
            placeholder="1234 5678 9012 3456"
            class="w-full p-2 lg:p-3 bg-secondary focus:outline-none focus:ring-2 focus:ring-accent border-2 border-fon rounded-lg text-sm lg:text-base"
        />
        <p v-if="errors.cardNumber" class="text-red-500 text-xs lg:text-sm">{{ errors.cardNumber }}</p>
      </div>
      <div>
        <label for="expiryDate" class="block text-sm lg:text-base font-medium text-text">Срок действия</label>
        <input
            type="text"
            id="expiryDate"
            v-model="form.expiryDate"
            placeholder="MM/YY"
            class="w-full p-2 lg:p-3 bg-secondary focus:outline-none focus:ring-2 focus:ring-accent border-2 border-fon rounded-lg text-sm lg:text-base"
        />
        <p v-if="errors.expiryDate" class="text-red-500 text-xs lg:text-sm">{{ errors.expiryDate }}</p>
      </div>
      <div>
        <label for="cvv" class="block text-sm lg:text-base font-medium text-text">CVV</label>
        <input
            type="text"
            id="cvv"
            v-model="form.cvv"
            placeholder="123"
            class="w-full p-2 lg:p-3 bg-secondary focus:outline-none focus:ring-2 focus:ring-accent border-2 border-fon rounded-lg text-sm lg:text-base"
        />
        <p v-if="errors.cvv" class="text-red-500 text-xs lg:text-sm">{{ errors.cvv }}</p>
      </div>
      <button
          type="submit"
          class="w-full py-2 lg:py-3 bg-accent text-secondary rounded-lg font-medium text-sm lg:text-base hover:bg-accent_hover transition-colors"
      >
        Оплатить
      </button>
    </form>
  </main>
</template>

<script setup>
import {ref, computed, onMounted} from 'vue';
import {useRouter} from 'vue-router';
import {useSubscriptionStore} from '@/stores/subscriptionStore';
import api from "@/api/index.js";

const router = useRouter();
const subscriptionStore = useSubscriptionStore();

// Извлечение ID подписки из параметров URL
const subId = new URLSearchParams(window.location.search).get('sub_id');
const selectedSubscription = computed(() => {
  return subscriptionStore.getSubscriptionById(Number(subId));
});

// Данные формы
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

// Отправка данных формы
const submitPayment = async () => {
  if (!validateForm()) return;

  try {
    await api.post(`/api/subscriptions/subscribe/${subId}`, form.value);
    await subscriptionStore.checkCurrentSubscription();
    await router.push('/premium');
  } catch (error) {
    console.error('Ошибка при оплате:', error);
    alert('Произошла ошибка при оплате.');
  }
};

// Загрузка подписок при монтировании компонента
onMounted(async () => {
  if (!subscriptionStore.subscriptions.length) {
    try {
      const response = await api.get('/api/subscriptions');
      subscriptionStore.setSubscriptions(response.data);
    } catch (error) {
      console.error('Ошибка загрузки подписок:', error);
    }
  }
});
</script>