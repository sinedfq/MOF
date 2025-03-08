<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// Состояние для новой подкатегории
const newSubcategory = ref({
  name: '',
  categoryId: null, // ID выбранной категории
});

// Список категорий для выбора
const categories = ref([]);

// Загрузка списка категорий
const fetchCategories = async () => {
  try {
    const response = await axios.get('/api/categories/');
    categories.value = response.data;
  } catch (error) {
    console.error('Ошибка при загрузке категорий:', error);
  }
};

// Функция для добавления новой подкатегории
const addSubcategory = async () => {
  try {
    // Проверяем, что категория выбрана
    if (!newSubcategory.value.categoryId) {
      alert('Пожалуйста, выберите категорию.');
      return;
    }

    // Подготовка данных для отправки
    const payload = {
      name: newSubcategory.value.name,
      category: newSubcategory.value.categoryId, // Отправляем ID категории
    };

    // Отправка данных на сервер
    const response = await axios.post('/api/subcategories/', payload, {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    console.log('Подкатегория успешно добавлена:', response.data);

    // Сброс формы
    newSubcategory.value = {
      name: '',
      categoryId: null,
    };

    alert('Подкатегория успешно добавлена!');
  } catch (error) {
    console.error('Ошибка при добавлении подкатегории:', error);
    alert('Не удалось добавить подкатегорию. Пожалуйста, попробуйте снова.');
  }
};

// Загружаем категории при монтировании компонента
onMounted(() => {
  fetchCategories();
});
</script>

<template>
  <div>
    <h2>Добавление новой Подкатегории</h2>
    <form @submit.prevent="addSubcategory">
      <div>
        <label for="subcategoryName">Название подкатегории:</label>
        <input
          id="subcategoryName"
          v-model="newSubcategory.name"
          required
        />
      </div>
      <div>
        <label for="subcategoryCategory">Категория:</label>
        <select
          id="subcategoryCategory"
          v-model="newSubcategory.categoryId"
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
      <button type="submit">Добавить</button>
    </form>
  </div>
</template>