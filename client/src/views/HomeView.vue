<script setup>
import { onBeforeMount, ref, computed } from 'vue';
import { useTransactionsStore } from '../stores/tranc';
import _ from 'lodash';
import TransRow from '@/components/TransRow.vue'; // Импортируем новый компонент

const transStore = useTransactionsStore();
const isAsc = ref(true);
const sortField = ref('created_date');

onBeforeMount(async () => {
    await transStore.fetchTrans();
});

const sortedTransactions = computed(() => {
    const order = isAsc.value ? 'asc' : 'desc';
    return _.orderBy(transStore.transactions, [sortField.value], [order]);
});

function toggleSort(field) {
    if (sortField.value === field) {
        isAsc.value = !isAsc.value;
    } else {
        sortField.value = field;
        isAsc.value = true;
    }
}
</script>

<template>
    <h1>Главная страница</h1>
    <button @click="toggleSort('created_date')">Сортировать по Дате Создания</button>
    <button @click="toggleSort('type.name')">Сортировать по Типу</button>
    <button @click="toggleSort('category.name')">Сортировать по Категории</button>
    <button @click="toggleSort('subcategory.name')">Сортировать по Подкатегории</button>

    <!-- Используем новый компонент -->
    <TransRow :sortedTransactions="sortedTransactions" />
</template>
