<script setup>
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';

// Состояние для новой транзакции
const newTransaction = ref({
  amount: 0,
  typeId: null,
  categoryId: null,
  subcategoryId: null,
  statusId: null,
  comment: '',
});

// Списки для выбора
const types = ref([]);
const categories = ref([]);
const subcategories = ref([]);
const statuses = ref([]);

// Загрузка списков (типы, категории, статусы)
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

// Следим за изменением категории
watch(
  () => newTransaction.value.categoryId,
  (newCategoryId) => {
    if (newCategoryId) {
      fetchSubcategories(newCategoryId);
    } else {
      subcategories.value = [];
    }
  }
);

const addTransaction = async () => {
  try {
    // Проверяем, что все обязательные поля заполнены
    if (
      !newTransaction.value.amount ||
      !newTransaction.value.typeId ||
      !newTransaction.value.categoryId ||
      !newTransaction.value.statusId
    ) {
      alert('Пожалуйста, заполните все обязательные поля.');
      return;
    }

    // Подготовка данных для отправки
    const payload = {
      status_id: newTransaction.value.statusId,  // Отправляем только ID
      category_id: newTransaction.value.categoryId,  // Отправляем только ID
      subcategory_id: newTransaction.value.subcategoryId,  // Отправляем только ID
      type_id: newTransaction.value.typeId,  // Отправляем только ID
      amount: newTransaction.value.amount,
      comment: newTransaction.value.comment,
    };

    console.log("Sending payload:", payload);  // Логируем данные перед отправкой

    // Отправка данных на сервер с использованием fetch
    const response = await fetch('/api/transitions/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(`Ошибка сервера: ${response.status} - ${JSON.stringify(errorData)}`);
    }

    const responseData = await response.json();
    console.log('Транзакция успешно добавлена:', responseData);

    // Сброс формы
    newTransaction.value = {
      amount: 0,
      typeId: null,
      categoryId: null,
      subcategoryId: null,
      statusId: null,
      comment: '',
    };

    alert('Транзакция успешно добавлена!');
  } catch (error) {
    console.error('Ошибка при добавлении транзакции:', error);
    alert('Не удалось добавить транзакцию. Пожалуйста, попробуйте снова.');
  }
};
// Загружаем данные при монтировании компонента
onMounted(async () => {
  await fetchInitialData();
});
</script>

<template>
  <div class="form-container">
    <h2 class="form-title">Добавление новой Транзакции</h2>
    <form @submit.prevent="addTransaction" class="transaction-form">
      <div class="form-group">
        <label for="amount">Сумма:</label>
        <input
          id="amount"
          v-model.number="newTransaction.amount"
          type="number"
          step="0.01"
          required
          class="form-input"
        />
      </div>
      <div class="form-group">
        <label for="type">Тип:</label>
        <select
          id="type"
          v-model="newTransaction.typeId"
          required
          class="form-select"
        >
          <option value="" disabled>Выберите тип</option>
          <option
            v-for="type in types"
            :key="type.id"
            :value="type.id"
          >
            {{ type.name }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="category">Категория:</label>
        <select
          id="category"
          v-model="newTransaction.categoryId"
          required
          class="form-select"
        >
          <option value="" disabled>Выберите категорию</option>
          <option
            v-for="category in categories"
            :key="category.id"
            :value="category.id"
          >
            {{ category.name }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="subcategory">Подкатегория:</label>
        <select
          id="subcategory"
          v-model="newTransaction.subcategoryId"
          class="form-select"
        >
          <option value="" disabled>Выберите подкатегорию</option>
          <option
            v-for="subcategory in subcategories"
            :key="subcategory.id"
            :value="subcategory.id"
          >
            {{ subcategory.name }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="status">Статус:</label>
        <select
          id="status"
          v-model="newTransaction.statusId"
          required
          class="form-select"
        >
          <option value="" disabled>Выберите статус</option>
          <option
            v-for="status in statuses"
            :key="status.id"
            :value="status.id"
          >
            {{ status.name }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="comment">Комментарий:</label>
        <textarea
          id="comment"
          v-model="newTransaction.comment"
          class="form-textarea"
        ></textarea>
      </div>
      <button type="submit" class="form-button">Добавить</button>
    </form>
  </div>
</template>

<style scoped>
@import '@/assets/base.css';
</style>