<script setup>
import { ref } from 'vue';
import axios from 'axios';

// Состояние для нового типа
const newType = ref('');

// Функция для добавления нового типа
const addType = async () => {
  try {
    // Подготовка данных для отправки
    const payload = {
      name: newType.value, // Отправляем имя типа
    };

    // Отправка данных на сервер
    const response = await axios.post('/api/types/', payload, {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    console.log('Тип успешно добавлен:', response.data);

    // Сброс поля ввода
    newType.value = '';

    alert('Тип успешно добавлен!');
  } catch (error) {
    console.error('Ошибка при добавлении типа:', error);
    alert('Не удалось добавить тип. Пожалуйста, попробуйте снова.');
  }
};
</script>

<template>
  <div>
    <h2>Добавление нового Типа</h2>
    <form @submit.prevent="addType">
      <div>
        <label for="type">Тип:</label>
        <input id="type" v-model="newType" required />
      </div>
      <button type="submit">Добавить</button>
    </form>
  </div>
</template>