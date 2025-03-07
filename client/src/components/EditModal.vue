<script setup>
    import { ref } from 'vue';

    const isOpen = ref(false);
    const editedTransaction = ref({
    amount: 0,
    type: { name: '' },
    category: { name: '' },
    subcategory: { name: '' }
    });

    const openModal = (transaction) => {
    editedTransaction.value = { ...transaction };
    isOpen.value = true;
    };

    const closeModal = () => {
    isOpen.value = false;
    };

    const saveChanges = () => {
    // Здесь можно добавить логику для сохранения изменений
    console.log('Сохраненные данные:', editedTransaction.value);
    closeModal();
    };

    defineExpose({ openModal });
</script>

<template>
    <div v-if="isOpen" class="modal-overlay">
      <div class="modal-content">
        <h2>Редактировать транзакцию</h2>
        <form @submit.prevent="saveChanges">
          <div>
            <label for="amount">Сумма:</label>
            <input id="amount" v-model="editedTransaction.amount" type="number" required>
          </div>
          <div>
            <label for="type">Тип:</label>
            <input id="type" v-model="editedTransaction.type.name" type="text" required>
          </div>
          <div>
            <label for="category">Категория:</label>
            <input id="category" v-model="editedTransaction.category.name" type="text" required>
          </div>
          <div>
            <label for="subcategory">Подкатегория:</label>
            <input id="subcategory" v-model="editedTransaction.subcategory.name" type="text" required>
          </div>
          <button type="submit">Сохранить</button>
          <button type="button" @click="closeModal">Закрыть</button>
        </form>
      </div>
    </div>
  </template>
  
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
    animation: fade-in ease-in-out 0.5s;

  }

  @keyframes fade-in {
    0%{
        margin-top: -10px;
        opacity: 0%;
    }
    100% {
        margin-top: 0px;
        opacity: 100%;
    }
  }

  @keyframes fade-out {
    0%{
        margin-top: 0px;
        opacity: 100%;
    }
    100% {
        margin-top: -5px;
        opacity: 0%;
    }
  }
  
  .modal-content {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    width: 300px;
  }
</style>