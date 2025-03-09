<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// Состояние для новой подкатегории
const newSubcategory = ref({
  name: '',
  categoryId: null,
});

// Состояние для редактируемой подкатегории
const editSubcategory = ref({
  id: null,
  name: '',
  categoryId: null,
});

// Список категорий для выбора
const categories = ref([]);

// Список подкатегорий
const subcategories = ref([]);

// Загрузка списка категорий
const fetchCategories = async () => {
  try {
    const response = await axios.get('/api/categories/');
    categories.value = response.data;
  } catch (error) {
    console.error('Ошибка при загрузке категорий:', error);
  }
};

// Загрузка списка подкатегорий
const fetchSubcategories = async () => {
  try {
    const response = await axios.get('/api/subcategories/');
    subcategories.value = response.data.map(subcategory => {
      // Находим категорию по ID
      const category = categories.value.find(cat => cat.id === subcategory.category);
      return {
        ...subcategory,
        categoryName: category ? category.name : 'Категория не найдена', // Добавляем имя категории
      };
    });
    console.log('Подкатегории загружены:', subcategories.value); // Логируем данные
  } catch (error) {
    console.error('Ошибка при загрузке подкатегорий:', error);
  }
};

// Функция для добавления новой подкатегории
const addSubcategory = async () => {
  try {
    if (!newSubcategory.value.categoryId) {
      alert('Пожалуйста, выберите категорию.');
      return;
    }

    const payload = {
      name: newSubcategory.value.name,
      category: newSubcategory.value.categoryId,
    };

    const response = await axios.post('/api/subcategories/', payload, {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    console.log('Подкатегория успешно добавлена:', response.data);

    newSubcategory.value = {
      name: '',
      categoryId: null,
    };

    alert('Подкатегория успешно добавлена!');
    fetchSubcategories(); // Обновляем список подкатегорий
  } catch (error) {
    console.error('Ошибка при добавлении подкатегории:', error);
    alert('Не удалось добавить подкатегорию. Пожалуйста, попробуйте снова.');
  }
};

// Функция для начала редактирования подкатегории
const startEdit = (subcategory) => {
  editSubcategory.value = {
    id: subcategory.id,
    name: subcategory.name,
    categoryId: subcategory.category, // Используем ID категории
  };
};

// Функция для сохранения изменений подкатегории
const saveEdit = async () => {
  try {
    const payload = {
      name: editSubcategory.value.name,
      category: editSubcategory.value.categoryId,
    };

    const response = await axios.put(`/api/subcategories/${editSubcategory.value.id}/`, payload, {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    console.log('Подкатегория успешно обновлена:', response.data);

    editSubcategory.value = {
      id: null,
      name: '',
      categoryId: null,
    };

    alert('Подкатегория успешно обновлена!');
    fetchSubcategories(); // Обновляем список подкатегорий
  } catch (error) {
    console.error('Ошибка при обновлении подкатегории:', error);
    alert('Не удалось обновить подкатегорию. Пожалуйста, попробуйте снова.');
  }
};

// Функция для отмены редактирования
const cancelEdit = () => {
  editSubcategory.value = {
    id: null,
    name: '',
    categoryId: null,
  };
};

// Загружаем категории и подкатегории при монтировании компонента
onMounted(async () => {
  await fetchCategories(); // Сначала загружаем категории
  await fetchSubcategories(); // Затем загружаем подкатегории
});
</script>

<template>
  <div class="form-container">
    <h2 class="form-title">Добавление новой Подкатегории</h2>
    <form @submit.prevent="addSubcategory" class="transaction-form">
      <div class="form-group">
        <label for="subcategoryName" class="form-label">Название подкатегории:</label>
        <input
          id="subcategoryName"
          v-model="newSubcategory.name"
          required
          class="form-input"
        />
      </div>
      <div class="form-group">
        <label for="subcategoryCategory">Категория:</label>
        <select
          id="subcategoryCategory"
          v-model="newSubcategory.categoryId"
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
      <button type="submit" class="form-button">Добавить</button>
    </form>

    <h2 class="form-title">Список Подкатегорий</h2>
    <table class="statuses-table">
      <thead>
        <tr>
          <th>Название</th>
          <th>Категория</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="subcategory in subcategories" :key="subcategory.id">
          <td>{{ subcategory.name }}</td>
          <td>{{ subcategory.categoryName }}</td> <!-- Используем categoryName -->
          <td>
            <button @click="startEdit(subcategory)" class="edit-button">Редактировать</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="editSubcategory.id" class="edit-form-container">
      <h2 class="form-title">Редактирование Подкатегории</h2>
      <form @submit.prevent="saveEdit" class="transaction-form">
        <div class="form-group">
          <label for="editSubcategoryName">Название подкатегории:</label>
          <input
            id="editSubcategoryName"
            v-model="editSubcategory.name"
            required
            class="form-input"
          />
        </div>
        <div class="form-group">
          <label for="editSubcategoryCategory">Категория:</label>
          <select
            id="editSubcategoryCategory"
            v-model="editSubcategory.categoryId"
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
        <button type="submit" class="form-button">Сохранить</button>
        <button type="button" @click="cancelEdit" class="cancel-button">Отмена</button>
      </form>
    </div>
  </div>
</template>

<style scoped>
@import '@/assets/base.css';
</style>