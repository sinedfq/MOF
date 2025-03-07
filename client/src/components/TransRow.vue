<script setup>
import { defineProps } from 'vue';

const props = defineProps({
    sortedTransactions: {
        type: Array,
        required: true
    }
});
</script>

<template>
    <ul>
        <li v-for="transaction in sortedTransactions" :key="transaction.id">
            <span>Дата: {{ transaction.created_date || 'Нет данных' }}</span>
            <span> | Айди {{ transaction.id || 'Нет данных' }} </span>
            <span> | Сумма {{ transaction.amount || 'Нет данных' }} </span>
            <span> | Тип {{ transaction.type?.name || 'Нет данных' }} </span>
            <span> | Категория {{ transaction.category?.name || 'Нет данных' }} </span>
            <span> | Подкатегория {{ transaction.subcategory?.name || 'Нет данных' }} </span>
        </li>
    </ul>
</template>
