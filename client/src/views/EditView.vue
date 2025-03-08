<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const transactionId = route.params.transactionId;

// Состояние для данных транзакции
const transaction = ref({
  amount: 0,
  type: null,
  category: null,
  subcategory: null,
  status: null,
  comment: '',
});

// Списки для выбора
const types = ref([]);
const categories = ref([]);
const subcategories = ref([]);
const statuses = ref([]);

// Загрузка данных транзакции
const fetchTransaction = async () => {
  try {
    console.log('Fetching transaction from:', `/api/transitions/${transactionId}/`);
    const response = await axios.get(`/api/transitions/${transactionId}/`);
    transaction.value = response.data;
  } catch (error) {
    console.error('Ошибка при загрузке транзакции:', error);
  }
};
// Загрузка списков (типы, категории, подкатегории, статусы)
const fetchInitialData = async () => {
  try {
    const [typesResponse, categoriesResponse, statusesResponse] = await Promise.all([
      axios.get('/api/types/'),
      axios.get('/api/categories/'),
      axios.get('/api/status/'),
    ]);
    types.value = typesResponse.data;
    categories.value = categoriesResponse.data;
    statuses.value = statusesResponse.data;
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
};

// Загрузка подкатегорий по выбранной категории
const fetchSubcategories = async (categoryId) => {
  if (!categoryId) {
    subcategories.value = [];
    return;
  }
  try {
    const response = await axios.get(`/api/subcategories/by-category/${categoryId}/`);
    subcategories.value = response.data;
  } catch (error) {
    console.error('Ошибка при загрузке подкатегорий:', error);
  }
};
// Валидация подкатегории по категории
const validateSubcategory = () => {
  if (
    transaction.value.subcategory &&
    transaction.value.category &&
    transaction.value.subcategory.category !== transaction.value.category.id
  ) {
    alert('Выбранная подкатегория не соответствует категории.');
    transaction.value.subcategory = null; // Сбросить подкатегорию
  }
};

// Следим за изменением категории
watch(
  () => transaction.value.category,
  (newCategory) => {
    if (newCategory) {
      fetchSubcategories(newCategory.id);
    } else {
      subcategories.value = [];
    }
    validateSubcategory();
  }
);

// Сохранение изменений
const saveTransaction = async () => {
  try {
    const payload = {
      ...transaction.value,
      type: transaction.type?.id,
      category: transaction.category?.id,
      subcategory: transaction.subcategory?.id,
      status: transaction.status?.id,
    };
    await axios.patch(`/api/transitions/${transactionId}/`, payload);
    alert('Транзакция успешно обновлена!');
  } catch (error) {
    console.error('Ошибка при обновлении транзакции:', error);
    alert('Не удалось обновить транзакцию. Пожалуйста, попробуйте снова.');
  }
};

// Загружаем данные при монтировании компонента
onMounted(async () => {
  await fetchInitialData();
  await fetchTransaction();
  if (transaction.value.category) {
    await fetchSubcategories(transaction.value.category.id);
  }
});
</script>

<template>
  <div>
    <h1>Редактирование транзакции #{{ transactionId }}</h1>

    <!-- Поле для суммы -->
    <div>
      <label for="amount">Сумма:</label>
      <input
        id="amount"
        v-model.number="transaction.amount"
        type="number"
        step="0.01"
        placeholder="Введите сумму"
      />
    </div>

    <!-- Поле для типа -->
    <div>
      <label for="type">Тип:</label>
      <select id="type" v-model="transaction.type">
        <option v-for="type in types" :key="type.id" :value="type">
          {{ type.name }}
        </option>
      </select>
    </div>

    <!-- Поле для категории -->
    <div>
      <label for="category">Категория:</label>
      <select id="category" v-model="transaction.category">
        <option v-for="category in categories" :key="category.id" :value="category">
          {{ category.name }}
        </option>
      </select>
    </div>

    <!-- Поле для подкатегории -->
    <div>
      <label for="subcategory">Подкатегория:</label>
      <select id="subcategory" v-model="transaction.subcategory">
        <option v-for="subcategory in subcategories" :key="subcategory.id" :value="subcategory">
          {{ subcategory.name }}
        </option>
      </select>
    </div>

    <!-- Поле для статуса -->
    <div>
      <label for="status">Статус:</label>
      <select id="status" v-model="transaction.status">
        <option v-for="status in statuses" :key="status.id" :value="status">
          {{ status.name }}
        </option>
      </select>
    </div>

    <!-- Поле для комментария -->
    <div>
      <label for="comment">Комментарий:</label>
      <textarea
        id="comment"
        v-model="transaction.comment"
        placeholder="Введите комментарий"
      ></textarea>
    </div>

    <!-- Кнопка для сохранения -->
    <button @click="saveTransaction">Сохранить</button>
  </div>
</template>

<style scoped>
div {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

input,
select,
textarea {
  width: 100%;
  padding: 0.5rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #369f6e;
}
</style>