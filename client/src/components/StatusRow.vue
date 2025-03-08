<script setup>
import { ref } from 'vue';
import axios from 'axios';

// Состояние для нового статуса
const newStatus = ref('');

// Функция для добавления нового статуса
const addStatus = async () => {
  try {
    // Подготовка данных для отправки
    const payload = {
      name: newStatus.value, // Отправляем имя статуса
    };

    // Отправка данных на сервер
    const response = await axios.post('/api/status/', payload, {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    console.log('Статус успешно добавлен:', response.data);

    // Сброс поля ввода
    newStatus.value = '';

    alert('Статус успешно добавлен!');
  } catch (error) {
    console.error('Ошибка при добавлении статуса:', error);
    alert('Не удалось добавить статус. Пожалуйста, попробуйте снова.');
  }
};
</script>

<template>
  <div>
    <h2>Добавление нового Статуса</h2>
    <form @submit.prevent="addStatus">
      <div>
        <label for="status">Статус:</label>
        <input id="status" v-model="newStatus" required />
      </div>
      <button type="submit">Добавить</button>
    </form>
  </div>
</template>