<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// Состояние для нового статуса
const newStatus = ref('');

// Состояние для редактируемого статуса
const editStatus = ref({
  id: null,
  name: '',
});

// Список статусов
const statuses = ref([]);

// Загрузка списка статусов
const fetchStatuses = async () => {
  try {
    const response = await axios.get('/api/status/');
    statuses.value = response.data;
  } catch (error) {
    console.error('Ошибка при загрузке статусов:', error);
  }
};

// Функция для добавления нового статуса
const addStatus = async () => {
  try {
    const payload = {
      name: newStatus.value,
    };

    const response = await axios.post('/api/status/', payload, {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    console.log('Статус успешно добавлен:', response.data);

    newStatus.value = '';
    alert('Статус успешно добавлен!');
    fetchStatuses(); // Обновляем список статусов
  } catch (error) {
    console.error('Ошибка при добавлении статуса:', error);
    alert('Не удалось добавить статус. Пожалуйста, попробуйте снова.');
  }
};

// Функция для начала редактирования статуса
const startEdit = (status) => {
  editStatus.value = {
    id: status.id,
    name: status.name,
  };
};

// Функция для сохранения изменений статуса
const saveEdit = async () => {
  try {
    const payload = {
      name: editStatus.value.name,
    };

    const response = await axios.put(`/api/status/${editStatus.value.id}/`, payload, {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    console.log('Статус успешно обновлен:', response.data);

    editStatus.value = {
      id: null,
      name: '',
    };

    alert('Статус успешно обновлен!');
    fetchStatuses(); // Обновляем список статусов
  } catch (error) {
    console.error('Ошибка при обновлении статуса:', error);
    alert('Не удалось обновить статус. Пожалуйста, попробуйте снова.');
  }
};

// Функция для отмены редактирования
const cancelEdit = () => {
  editStatus.value = {
    id: null,
    name: '',
  };
};

// Загружаем статусы при монтировании компонента
onMounted(() => {
  fetchStatuses();
});
</script>

<template>
  <div class="form-container">
    <h2 class="form-title">Добавление нового Статуса</h2>
    <form @submit.prevent="addStatus" class="transaction-form">
      <div class="form-group">
        <label for="status" class="form-label">Статус:</label>
        <input id="status" v-model="newStatus" required class="form-input" />
      </div>
      <button type="submit" class="form-button">Добавить</button>
    </form>

    <h2 class="form-title">Список Статусов</h2>
    <table class="statuses-table">
      <thead>
        <tr>
          <th>Название</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="status in statuses" :key="status.id">
          <td>{{ status.name }}</td>
          <td>
            <button @click="startEdit(status)" class="edit-button">Редактировать</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="editStatus.id" class="edit-form-container">
      <h2 class="form-title">Редактирование Статуса</h2>
      <form @submit.prevent="saveEdit" class="transaction-form">
        <div class="form-group">
          <label for="editStatusName">Название статуса:</label>
          <input
            id="editStatusName"
            v-model="editStatus.name"
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

<style scoped>
@import '@/assets/base.css';

</style>