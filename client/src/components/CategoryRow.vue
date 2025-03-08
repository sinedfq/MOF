<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// Состояние для новой категории
const newCategory = ref({
  name: '',
  typeId: null, // ID выбранного типа
});

// Список типов для выбора
const types = ref([]);

// Загрузка списка типов
const fetchTypes = async () => {
  try {
    const response = await axios.get('/api/types/');
    types.value = response.data;
  } catch (error) {
    console.error('Ошибка при загрузке типов:', error);
  }
};

// Функция для добавления новой категории
const addCategory = async () => {
  try {
    // Проверяем, что тип выбран
    if (!newCategory.value.typeId) {
      alert('Пожалуйста, выберите тип.');
      return;
    }

    // Подготовка данных для отправки
    const payload = {
      name: newCategory.value.name,
      type: newCategory.value.typeId, // Отправляем ID типа
    };

    // Отправка данных на сервер
    const response = await axios.post('/api/categories/', payload, {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    console.log('Категория успешно добавлена:', response.data);

    // Сброс формы
    newCategory.value = {
      name: '',
      typeId: null,
    };

    alert('Категория успешно добавлена!');
  } catch (error) {
    console.error('Ошибка при добавлении категории:', error);
    alert('Не удалось добавить категорию. Пожалуйста, попробуйте снова.');
  }
};

// Загружаем типы при монтировании компонента
onMounted(() => {
  fetchTypes();
});
</script>

<template>
  <div>
    <h2>Добавление новой Категории</h2>
    <form @submit.prevent="addCategory">
      <div>
        <label for="categoryName">Название категории:</label>
        <input
          id="categoryName"
          v-model="newCategory.name"
          required
        />
      </div>
      <div>
        <label for="categoryType">Тип:</label>
        <select
          id="categoryType"
          v-model="newCategory.typeId"
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
      <button type="submit">Добавить</button>
    </form>
  </div>
</template>