<template>
  <main class="min-h-screen bg-fon p-4 sm:p-8">
    <Notification
        v-if="notificationStore.isVisible"
        :type="notificationStore.type"
        :message="notificationStore.message"
        @close="notificationStore.hideNotification"
    />
    <h1 class="text-2xl sm:text-3xl font-bold text-text mb-6">Админ панель Gamers</h1>

    <div class="grid grid-cols-1 lg:grid-cols-[250px_1fr] gap-5">
      <!-- Левая колонка - навигация по таблицам -->
      <nav aria-label="Навигация по таблицам" class="bg-secondary rounded-lg p-4 h-fit">
        <h2 class="text-xl font-semibold mb-4">Таблицы</h2>
        <ul class="space-y-2">
          <li v-for="table in tables" :key="table.value">
            <button
                class="block w-full p-2 bg-primary hover:bg-primary_hover text-text rounded-lg transition text-left"
                @click="selectTable(table)"
                :aria-current="selectedTable?.value === table.value ? 'page' : null"
            >
              {{ table.label }}
            </button>
          </li>
        </ul>
      </nav>

      <!-- Правая колонка - содержимое таблицы -->
      <section class="bg-secondary rounded-lg p-4 overflow-x-auto">
        <header class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-4">
          <h2 class="text-xl font-semibold">{{ selectedTable?.label }}</h2>
          <button
              v-if="selectedTable?.canCreate !== false"
              @click="openCreateModal"
              class="p-2 bg-accent hover:bg-accent_hover text-secondary rounded-lg transition font-semibold whitespace-nowrap"
              aria-label="Добавить новую запись"
          >
            Добавить запись
          </button>
        </header>

        <div v-if="isLoading" class="flex justify-center items-center py-8">
          <p class="text-text">Загрузка данных...</p>
        </div>

        <div v-else-if="selectedTable">
          <div class="overflow-x-auto">
            <table class="w-full border-collapse text-sm sm:text-base min-w-[600px]">
              <thead class="bg-primary">
              <tr>
                <th
                    v-for="column in displayColumns"
                    :key="column.field"
                    class="p-2 sm:p-3 text-left border border-text/70"
                >
                  {{ column.label }}
                </th>
                <th class="p-2 sm:p-3 text-left border border-text/70">Действия</th>
              </tr>
              </thead>
              <tbody>
              <tr v-for="(row, index) in data" :key="index" class="hover:bg-primary/10">
                <td
                    v-for="column in displayColumns"
                    :key="column.field"
                    class="p-2 sm:p-3 border border-text/70 align-middle break-words max-w-[200px]"
                >
                  {{ row[column.field] }}
                </td>
                <td class="p-2 sm:p-3 border border-text/70 align-middle">
                  <div class="flex gap-2 items-center">
                    <button
                        @click="openEditModal(row)"
                        class="p-1 text-accent hover:text-accent_hover transition"
                        title="Редактировать"
                        aria-label="Редактировать запись"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none"
                           stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                        <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                      </svg>
                    </button>
                    <button
                        @click="confirmDelete(row)"
                        class="p-1 text-red-500 hover:text-red-700 transition"
                        title="Удалить"
                        aria-label="Удалить запись"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none"
                           stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="3 6 5 6 21 6"></polyline>
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </div>

    <!-- Модальное окно создания/редактирования -->
    <div
        v-if="isModalOpen"
        class="fixed inset-0 bg-black bg-opacity-70 flex justify-center items-center z-50 p-4"
        @click.self="closeModal"
    >
      <div class="bg-fon p-6 rounded-lg w-full max-w-md">
        <div class="mb-4">
          <h2 class="text-xl lg:text-2xl font-semibold text-text text-center">
            {{ isEditing ? 'Редактирование' : 'Создание' }} записи
          </h2>
        </div>

        <form @submit.prevent="submitForm" class="space-y-4">
          <div v-for="column in formColumns" :key="column.field">
            <label class="block text-sm lg:text-base text-text mb-1">{{ column.label }}</label>

            <!-- Текстовое поле -->
            <input
                v-if="column.type === 'text'"
                v-model="currentRecord[column.field]"
                type="text"
                class="w-full p-2 text-sm lg:text-base rounded-lg bg-secondary border-2 border-fon focus:outline-none focus:ring-2 focus:ring-primary text-text"
                :required="column.required"
                :minlength="column.minLength"
                :maxlength="column.maxLength"
            />

            <!-- Числовое поле -->
            <input
                v-else-if="column.type === 'number'"
                v-model.number="currentRecord[column.field]"
                type="number"
                class="w-full p-2 text-sm lg:text-base rounded-lg bg-secondary border-2 border-fon focus:outline-none focus:ring-2 focus:ring-primary text-text"
                :required="column.required"
                :min="column.min"
                :step="column.step"
            />

            <!-- Стандартное поле -->
            <input
                v-else
                v-model="currentRecord[column.field]"
                :type="column.type || 'text'"
                class="w-full p-2 text-sm lg:text-base rounded-lg bg-secondary border-2 border-fon focus:outline-none focus:ring-2 focus:ring-primary text-text"
                :required="column.required"
            />
          </div>

          <div class="flex justify-between gap-4 pt-2">
            <button
                type="button"
                @click="closeModal"
                class="flex-1 p-2 bg-secondary hover:bg-secondary_hover text-text rounded-lg transition font-medium text-sm lg:text-base"
            >
              Отменить
            </button>
            <button
                type="submit"
                class="flex-1 p-2 bg-accent hover:bg-accent_hover text-secondary rounded-lg transition font-medium text-sm lg:text-base"
            >
              {{ isEditing ? 'Сохранить' : 'Создать' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Модальное окно подтверждения удаления -->
    <div
        v-if="isDeleteConfirmOpen"
        class="fixed inset-0 bg-black bg-opacity-70 flex justify-center items-center z-50 p-4"
        @click.self="closeDeleteModal"
    >
      <div class="bg-fon p-6 rounded-lg w-full max-w-md">
        <div class="mb-4">
          <h2 class="text-xl lg:text-2xl font-semibold text-text text-center">Подтверждение удаления</h2>
        </div>

        <p class="text-text mb-6 text-center">Вы уверены, что хотите удалить эту запись?</p>

        <div class="flex justify-between gap-4">
          <button
              @click="closeDeleteModal"
              class="flex-1 p-2 bg-secondary hover:bg-secondary_hover text-text rounded-lg transition font-medium text-sm lg:text-base"
          >
            Отменить
          </button>
          <button
              @click="deleteRecord"
              class="flex-1 p-2 bg-red-500 hover:bg-red-700 text-white rounded-lg transition font-medium text-sm lg:text-base"
          >
            Удалить
          </button>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import {ref, onMounted, computed} from 'vue';
import api from '@/api';
import Notification from "@/components/Notification.vue";
import {useNotificationStore} from '@/stores/notificationStore';

const notificationStore = useNotificationStore();

const tables = ref([
  {
    value: 'users',
    label: 'Пользователи',
    endpoint: '/api/auth/users',
    canCreate: false,
    columns: [
      {field: 'id', label: 'ID', type: 'number', showInTable: true, showInForm: false},
      {
        field: 'username',
        label: 'Имя пользователя',
        type: 'text',
        showInTable: true,
        showInForm: true,
        required: true,
        minLength: 3,
        maxLength: 60
      },
      {
        field: 'email',
        label: 'Email',
        type: 'email',
        showInTable: true,
        showInForm: true,
        required: true
      },
      {
        field: 'avatar',
        label: 'Аватар',
        type: 'text',
        showInTable: false,
        showInForm: true
      },
      {
        field: 'is_active',
        label: 'Активен',
        type: 'checkbox',
        showInTable: true,
        showInForm: true
      },
      {
        field: 'is_admin',
        label: 'Админ',
        type: 'checkbox',
        showInTable: true,
        showInForm: true
      },
      {
        field: 'created_at',
        label: 'Дата создания',
        type: 'date',
        showInTable: true,
        showInForm: false
      }
    ]
  },
  {
    value: 'games',
    label: 'Игры',
    endpoint: '/api/games',
    columns: [
      {field: 'id', label: 'ID', type: 'number', showInTable: true, showInForm: false},
      {
        field: 'name',
        label: 'Название',
        type: 'text',
        showInTable: true,
        showInForm: true,
        required: true,
        minLength: 1,
        maxLength: 100
      },
      {
        field: 'avatar',
        label: 'Аватар',
        type: 'text',
        showInTable: false,
        showInForm: true,
        description: "URL аватара игры"
      }
    ]
  },
  {
    value: 'game_types',
    label: 'Типы игр',
    endpoint: '/api/games/types',
    columns: [
      {field: 'id', label: 'ID', type: 'number', showInTable: true, showInForm: false},
      {
        field: 'name',
        label: 'Название',
        type: 'text',
        showInTable: true,
        showInForm: true,
        required: true,
        minLength: 1,
        maxLength: 100
      }
    ]
  },
  {
    value: 'subscriptions',
    label: 'Подписки',
    endpoint: '/api/subscriptions',
    columns: [
      {field: 'id', label: 'ID', type: 'number', showInTable: true, showInForm: false},
      {
        field: 'name',
        label: 'Название',
        type: 'text',
        showInTable: true,
        showInForm: true,
        required: true,
        minLength: 1,
        maxLength: 100
      },
      {
        field: 'price',
        label: 'Цена',
        type: 'number',
        showInTable: true,
        showInForm: true,
        required: true,
        min: 0.01,
        step: 0.01
      },
      {
        field: 'duration',
        label: 'Длительность (дни)',
        type: 'number',
        showInTable: true,
        showInForm: true,
        required: true,
        min: 1,
        step: 1
      }
    ]
  }
]);

const selectedTable = ref(tables.value[0]);
const data = ref([]);
const isModalOpen = ref(false);
const isDeleteConfirmOpen = ref(false);
const isEditing = ref(false);
const currentRecord = ref({});
const recordToDelete = ref(null);
const isLoading = ref(false);

// Колонки для отображения в таблице
const displayColumns = computed(() => {
  if (!selectedTable.value) return [];
  return selectedTable.value.columns.filter(column => column.showInTable);
});

// Колонки для формы
const formColumns = computed(() => {
  if (!selectedTable.value) return [];
  return selectedTable.value.columns.filter(column => column.showInForm);
});

// Закрытие модального окна
const closeModal = () => {
  isModalOpen.value = false;
  currentRecord.value = {};
};

// Загрузка данных при монтировании
onMounted(async () => {
  await fetchTableData(selectedTable.value);
});

// Выбор таблицы
const selectTable = async (table) => {
  selectedTable.value = table;
  await fetchTableData(table);
};

// Загрузка данных таблицы
const fetchTableData = async (table) => {
  isLoading.value = true;
  try {
    const response = await api.get(table.endpoint);
    data.value = response.data;
  } catch (error) {
    console.error('Ошибка загрузки данных:', error);
    notificationStore.showNotification('error', 'Ошибка загрузки данных');
  } finally {
    isLoading.value = false;
  }
};

// Открытие модального окна создания
const openCreateModal = () => {
  currentRecord.value = {};
  formColumns.value.forEach(column => {
    currentRecord.value[column.field] = column.type === 'number' ? 0 :
        column.type === 'checkbox' ? false : '';
  });
  isEditing.value = false;
  isModalOpen.value = true;
};

// Открытие модального окна редактирования
const openEditModal = (row) => {
  currentRecord.value = {...row};
  isEditing.value = true;
  isModalOpen.value = true;
};

// Подтверждение удаления
const confirmDelete = (row) => {
  recordToDelete.value = row;
  isDeleteConfirmOpen.value = true;
};

// Закрытие модального окна подтверждения удаления
const closeDeleteModal = () => {
  isDeleteConfirmOpen.value = false;
};

// Удаление записи
const deleteRecord = async () => {
  try {
    await api.delete(`${selectedTable.value.endpoint}/${recordToDelete.value.id}`);
    await fetchTableData(selectedTable.value);
    isDeleteConfirmOpen.value = false;
    notificationStore.showNotification('success', 'Запись успешно удалена');
  } catch (error) {
    notificationStore.showNotification('error', 'Ошибка при удалении записи');
    console.error('Ошибка удаления:', error);
  }
};

// Отправка формы
const submitForm = async () => {
  try {
    const payload = {};
    formColumns.value.forEach(column => {
      if (currentRecord.value[column.field] !== undefined) {
        payload[column.field] = currentRecord.value[column.field];
      }
    });

    if (selectedTable.value.value === 'users') {
      delete payload.password;
      delete payload.confirm_password;
    }

    let actionMessage = '';
    if (isEditing.value) {
      await api.put(
          `${selectedTable.value.endpoint}/${currentRecord.value.id}`,
          payload
      );
      actionMessage = 'Запись успешно обновлена';
    } else {
      await api.post(
          selectedTable.value.endpoint,
          payload
      );
      actionMessage = 'Запись успешно создана';
    }

    await fetchTableData(selectedTable.value);
    notificationStore.showNotification('success', actionMessage);
    closeModal();
  } catch (error) {
    console.error('Ошибка сохранения:', error);
    let errorMessage = 'Ошибка при сохранении данных';
    notificationStore.showNotification('error', errorMessage);
  }
};
</script>