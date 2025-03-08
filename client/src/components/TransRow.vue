<script setup>
import { ref } from 'vue';

const props = defineProps({
  sortedTransactions: {
    type: Array,
    required: true
  },
  onDeleteClick: {
    type: Function,
    required: true
  }
});


</script>

<template>
  <ul>
    <li v-for="transaction in sortedTransactions" :key="transaction.id">
      <span>{{ transaction.id || 'Нет данных' }} </span>
      <span>{{ new Date(transaction.created_date).toLocaleString() || 'Нет данных' }}</span>
      <span>{{ transaction.amount || 'Нет данных' }} </span>
      <span>{{ transaction.type?.name || 'Нет данных' }} </span>
      <span>{{ transaction.category?.name || 'Нет данных' }} </span>
      <span>{{ transaction.subcategory?.name || 'Нет данных' }} </span>
      <nav>
        <RouterLink
          :to="{ name: 'edit', params: { transactionId: transaction.id } }"
          class="custom-button"
        >
          Редактировать
        </RouterLink>
      </nav>
      <button class="custom-button" @click ="onDeleteClick(transaction)" style="background-color: #FF7373">Удалить</button>
    </li>
  </ul>
  <button class="custom-button" style="margin-left: 93%">Добавить</button>

</template>

<style>
    ul {
    list-style-type: none; 
    padding: 0;
    margin: 0;
    }

    li {
    padding: 10px;
    background-color: #f0f0f0;
    transition: background-color 0.3s ease;
    display: flex; 
    justify-content: space-between; 
    align-items: center; 
    margin-bottom: 5px; 
    }

    li:hover {
    background-color: #ccc;
    cursor: pointer;
    }

    li span {
    flex: 1; 
    font-size: 14px;
    color: #333;
    padding: 5px; 
    text-align: center; 
    border-right: 1px solid #ccc; 
    }

    li span:last-child {
    border-right: none; 
    }
    
    .custom-button {
    position: relative;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 12px 12px;
    font-size: 15px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    outline: none;
    user-select: none;
    color: #000000;
    border-top-width: 0px;
    border-right-width: 0px;
    border-bottom-width: 0px;
    border-left-width: 0px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
    border-bottom-left-radius: 4px;
    background-color: #c3c3c3;
    box-shadow: 0px 4px 8px 0px rgba(0,0,0,0.2);
    margin-left: 10px;
    margin-bottom: 10px;
    }

    .custom-button:hover {
    transition: all 0.3s ease;
    transform: translateY(-4px);
    }

</style>