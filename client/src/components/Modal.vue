<template>
    <div v-if="isOpen" class="modal-overlay">
      <div class="modal-content">
        <h2>Добавить запись</h2>
        <form @submit.prevent="submitForm">
          <div>
            <label for="name">Имя:</label>
            <input id="name" v-model="formData.name" type="text" required>
          </div>
          <div>
            <label for="email">Email:</label>
            <input id="email" v-model="formData.email" type="email" required>
          </div>
          <button type="submit">Сохранить</button>
          <button type="button" @click="closeModal">Закрыть</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        isOpen: false,
        formData: {
          name: '',
          email: ''
        }
      };
    },
    methods: {
      openModal() {
        this.isOpen = true;
      },
      closeModal() {
        this.isOpen = false;
        this.formData = { name: '', email: '' }; // Очистка формы
      },
      async submitForm() {
        try {
          const response = await axios.post('/api/save-data', this.formData);
          console.log('Данные успешно сохранены:', response.data);
          this.closeModal();
        } catch (error) {
          console.error('Ошибка при сохранении данных:', error);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .modal-content {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    width: 300px;
  }
  </style>