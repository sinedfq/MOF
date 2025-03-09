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
  <!-- Шапка таблицы -->
  <div class="table-header">
    <span>ID</span>
    <span>Дата Создания</span>
    <span>Сумма</span>
    <span>Тип</span>
    <span>Категория</span>
    <span>Подкатегория</span>
    <span>Действия</span>
  </div>

  <!-- Список транзакций -->
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
      <button class="custom-button" @click="onDeleteClick(transaction)" style="background-color: #FF7373">Удалить</button>
    </li>
  </ul>
</template>

<!-- Подключаем стили -->
<style>
@import '@/assets/home.css';
</style>