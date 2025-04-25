<template>
  <div class="p-8 grid grid-cols-[250px_1fr] gap-8">
    <!-- Левый сайдбар с таблицами -->
    <aside class="bg-secondary rounded-lg p-4 h-fit">
      <h2 class="text-s20 font-semibold mb-4">Таблицы</h2>
      <ul class="space-y-2">
        <li v-for="table in tables" :key="table">
          <button
              class="block w-full p-2 bg-primary hover:bg-primary_hover text-text rounded-lg transition"
              @click="selectTable(table)"
          >
            {{ table }}
          </button>
        </li>
      </ul>
    </aside>

    <!-- Правая часть с содержимым таблицы -->
    <section class="bg-secondary rounded-lg p-4">
      <h2 class="text-s20 font-semibold mb-4">{{ selectedTable || 'Выберите таблицу' }}</h2>
      <table v-if="selectedTable" class="w-full border-collapse">
        <thead class="bg-primary">
        <tr>
          <th v-for="column in columns" :key="column" class="p-2 text-left border border-text/70">{{ column }}</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(row, index) in data" :key="index">
          <td v-for="column in columns" :key="column" class="p-2 border border-text/70">
            {{ row[column] }}
          </td>
        </tr>
        </tbody>
      </table>
    </section>
  </div>
</template>

<script setup>
import {ref, onMounted} from 'vue';
import api from '@/api';

const tables = ref([]);
const selectedTable = ref('users');
const columns = ref([]);
const data = ref([]);

// Загрузка списка таблиц
onMounted(async () => {
  try {
    const response = await api.get('/api/admin/tables');
    tables.value = response.data.tables;
    await fetchTableData('users');
  } catch (error) {
    console.error('Ошибка загрузки таблиц:', error);
  }
});

// Выбор таблицы
const selectTable = async (table) => {
  selectedTable.value = table;
  await fetchTableData(table);
};

// Загрузка данных для выбранной таблицы
const fetchTableData = async (table) => {
  try {
    const response = await api.get(`/api/admin/table/${table}`, {
      params: {
        limit: 10,
      }
    });
    columns.value = response.data.columns;
    data.value = response.data.data;
  } catch (error) {
    console.error('Ошибка загрузки данных таблицы:', error);
    // Для отладки выведем полный ответ сервера
    if (error.response) {
      console.error('Детали ошибки:', error.response.data);
    }
  }
};
</script>