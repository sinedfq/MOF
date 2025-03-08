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

// Добавление новой транзакции
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

    // Находим выбранные объекты по их ID
    const selectedType = types.value.find(type => type.id === newTransaction.value.typeId);
    const selectedCategory = categories.value.find(category => category.id === newTransaction.value.categoryId);
    const selectedSubcategory = subcategories.value.find(subcategory => subcategory.id === newTransaction.value.subcategoryId);
    const selectedStatus = statuses.value.find(status => status.id === newTransaction.value.statusId);

    // Подготовка данных для отправки
    const payload = {
      amount: newTransaction.value.amount,
      type: {
        name: selectedType ? selectedType.name : '', // Используем имя типа
      },
      category: {
        name: selectedCategory ? selectedCategory.name : '', // Используем имя категории
        type: null, // Если нужно, можно передать тип
      },
      subcategory: {
        name: selectedSubcategory ? selectedSubcategory.name : '', // Используем имя подкатегории
        category: null, // Если нужно, можно передать категорию
      },
      status: {
        name: selectedStatus ? selectedStatus.name : '', // Используем имя статуса
      },
      comment: newTransaction.value.comment,
    };

    // Отправка данных на сервер
    const response = await axios.post('/api/transitions/', payload, {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    console.log('Транзакция успешно добавлена:', response.data);

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
  <div>
    <h2>Добавление новой Транзакции</h2>
    <form @submit.prevent="addTransaction">
      <div>
        <label for="amount">Сумма:</label>
        <input
          id="amount"
          v-model.number="newTransaction.amount"
          type="number"
          step="0.01"
          required
        />
      </div>
      <div>
        <label for="type">Тип:</label>
        <select
          id="type"
          v-model="newTransaction.typeId"
          required
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
      <div>
        <label for="category">Категория:</label>
        <select
          id="category"
          v-model="newTransaction.categoryId"
          required
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
      <div>
        <label for="subcategory">Подкатегория:</label>
        <select
          id="subcategory"
          v-model="newTransaction.subcategoryId"
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
      <div>
        <label for="status">Статус:</label>
        <select
          id="status"
          v-model="newTransaction.statusId"
          required
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
      <div>
        <label for="comment">Комментарий:</label>
        <textarea
          id="comment"
          v-model="newTransaction.comment"
        ></textarea>
      </div>
      <button type="submit">Добавить</button>
    </form>
  </div>
</template>