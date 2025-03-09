<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// Состояние для новой категории
const newCategory = ref({
  name: '',
  typeId: null,
});

// Состояние для редактируемой категории
const editCategory = ref({
  id: null,
  name: '',
  typeId: null,
});

// Список типов для выбора
const types = ref([]);

// Список категорий
const categories = ref([]);

// Загрузка списка типов
const fetchTypes = async () => {
  try {
    const response = await axios.get('/api/types/');
    types.value = response.data;
  } catch (error) {
    console.error('Ошибка при загрузке типов:', error);
  }
};

// Загрузка списка категорий
const fetchCategories = async () => {
  try {
    const response = await axios.get('/api/categories/');
    categories.value = response.data.map(category => {
      // Находим тип по ID
      const type = types.value.find(t => t.id === category.type);
      return {
        ...category,
        typeName: type ? type.name : 'Тип не найден', // Добавляем имя типа
      };
    });
    console.log('Категории загружены:', categories.value); // Логируем данные
  } catch (error) {
    console.error('Ошибка при загрузке категорий:', error);
  }
};

// Функция для добавления новой категории
const addCategory = async () => {
  try {
    if (!newCategory.value.typeId) {
      alert('Пожалуйста, выберите тип.');
      return;
    }

    const payload = {
      name: newCategory.value.name,
      type: newCategory.value.typeId,
    };

    const response = await axios.post('/api/categories/', payload, {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    console.log('Категория успешно добавлена:', response.data);

    newCategory.value = {
      name: '',
      typeId: null,
    };

    alert('Категория успешно добавлена!');
    fetchCategories(); // Обновляем список категорий
  } catch (error) {
    console.error('Ошибка при добавлении категории:', error);
    alert('Не удалось добавить категорию. Пожалуйста, попробуйте снова.');
  }
};

// Функция для начала редактирования категории
const startEdit = (category) => {
  editCategory.value = {
    id: category.id,
    name: category.name,
    typeId: category.type, // Используем ID типа
  };
};

// Функция для сохранения изменений категории
const saveEdit = async () => {
  try {
    const payload = {
      name: editCategory.value.name,
      type: editCategory.value.typeId,
    };

    const response = await axios.put(`/api/categories/${editCategory.value.id}/`, payload, {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    console.log('Категория успешно обновлена:', response.data);

    editCategory.value = {
      id: null,
      name: '',
      typeId: null,
    };

    alert('Категория успешно обновлена!');
    fetchCategories(); // Обновляем список категорий
  } catch (error) {
    console.error('Ошибка при обновлении категории:', error);
    alert('Не удалось обновить категорию. Пожалуйста, попробуйте снова.');
  }
};

// Функция для отмены редактирования
const cancelEdit = () => {
  editCategory.value = {
    id: null,
    name: '',
    typeId: null,
  };
};

// Загружаем типы и категории при монтировании компонента
onMounted(async () => {
  await fetchTypes(); // Сначала загружаем типы
  await fetchCategories(); // Затем загружаем категории
});
</script>

<template>
  <div class="form-container">
    <h2 class="form-title">Добавление новой Категории</h2>
    <form @submit.prevent="addCategory" class="transaction-form">
      <div class="form-group">
        <label for="categoryName">Название категории:</label>
        <input
          id="categoryName"
          v-model="newCategory.name"
          required
          class="form-input"
        />
      </div>
      <div class="form-group">
        <label for="categoryType">Тип:</label>
        <select
          id="categoryType"
          v-model="newCategory.typeId"
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
      <button type="submit" class="form-button">Добавить</button>
    </form>

    <h2 class="form-title">Список Категорий</h2>
    <table class="statuses-table">
      <thead>
        <tr>
          <th>Название</th>
          <th>Тип</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="category in categories" :key="category.id">
          <td>{{ category.name }}</td>
          <td>{{ category.typeName }}</td> <!-- Используем typeName -->
          <td>
            <button @click="startEdit(category)" class="edit-button">Редактировать</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="editCategory.id" class="edit-form-container">
      <h2 class="form-title">Редактирование Категории</h2>
      <form @submit.prevent="saveEdit" class="transaction-form">
        <div class="form-group">
          <label for="editCategoryName">Название категории:</label>
          <input
            id="editCategoryName"
            v-model="editCategory.name"
            required
            class="form-input"
          />
        </div>
        <div class="form-group">
          <label for="editCategoryType">Тип:</label>
          <select
            id="editCategoryType"
            v-model="editCategory.typeId"
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
        <button type="submit" class="form-button">Сохранить</button>
        <button type="button" @click="cancelEdit" class="cancel-button">Отмена</button>
      </form>
    </div>
  </div>
</template>

<!-- Подключаем стили -->
<style scoped>
@import '@/assets/base.css';
</style>