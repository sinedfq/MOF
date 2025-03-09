<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// Состояние для нового типа
const newType = ref('');

// Состояние для редактируемого типа
const editType = ref({
  id: null,
  name: '',
});

// Список типов
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

// Функция для добавления нового типа
const addType = async () => {
  try {
    const payload = {
      name: newType.value,
    };

    const response = await axios.post('/api/types/', payload, {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    console.log('Тип успешно добавлен:', response.data);

    newType.value = '';
    alert('Тип успешно добавлен!');
    fetchTypes(); // Обновляем список типов
  } catch (error) {
    console.error('Ошибка при добавлении типа:', error);
    alert('Не удалось добавить тип. Пожалуйста, попробуйте снова.');
  }
};

// Функция для начала редактирования типа
const startEdit = (type) => {
  editType.value = {
    id: type.id,
    name: type.name,
  };
};

// Функция для сохранения изменений типа
const saveEdit = async () => {
  try {
    const payload = {
      name: editType.value.name,
    };

    const response = await axios.put(`/api/types/${editType.value.id}/`, payload, {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    console.log('Тип успешно обновлен:', response.data);

    editType.value = {
      id: null,
      name: '',
    };

    alert('Тип успешно обновлен!');
    fetchTypes(); // Обновляем список типов
  } catch (error) {
    console.error('Ошибка при обновлении типа:', error);
    alert('Не удалось обновить тип. Пожалуйста, попробуйте снова.');
  }
};

// Функция для отмены редактирования
const cancelEdit = () => {
  editType.value = {
    id: null,
    name: '',
  };
};

// Загружаем типы при монтировании компонента
onMounted(() => {
  fetchTypes();
});
</script>

<template>
  <div class="form-container">
    <h2 class="form-title">Добавление нового Типа</h2>
    <form @submit.prevent="addType" class="transaction-form">
      <div class="form-group">
        <label for="type" class="form-label">Тип:</label>
        <input id="type" v-model="newType" required class="form-input" />
      </div>
      <button type="submit" class="form-button">Добавить</button>
    </form>

    <h2 class="form-title">Список Типов</h2>
    <table class="statuses-table">
      <thead>
        <tr>
          <th>Название</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="type in types" :key="type.id">
          <td>{{ type.name }}</td>
          <td>
            <button @click="startEdit(type)" class="edit-button">Редактировать</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="editType.id" class="edit-form-container">
      <h2 class="form-title">Редактирование Типа</h2>
      <form @submit.prevent="saveEdit" class="transaction-form">
        <div class="form-group">
          <label for="editTypeName">Название типа:</label>
          <input
            id="editTypeName"
            v-model="editType.name"
            required
            class="form-input"
          />
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