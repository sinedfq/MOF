<script setup>
import { onBeforeMount, ref, computed } from 'vue';
import { useTransactionsStore } from '../stores/tranc';
import _ from 'lodash';
import TransRow from '@/components/TransRow.vue';

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

function onDeleteClick(transaction){
    transStore.delTrans(transaction.id)
}

</script>

<template>
    <div style="margin-left: 600px;">
        <button class = "custom-button" @click="toggleSort('created_date')">Сортировать по Дате Создания</button>
        <button class = "custom-button" @click="toggleSort('type.name')">Сортировать по Типу</button>
        <button class = "custom-button" @click="toggleSort('category.name')">Сортировать по Категории</button>
        <button class = "custom-button" @click="toggleSort('subcategory.name')">Сортировать по Подкатегории</button>
    </div>

    
    
    <TransRow 
        :sortedTransactions="sortedTransactions" 
        :onDeleteClick="onDeleteClick" />
    
        <RouterLink
          :to="{ name: 'add'}"
          class="custom-button"
        >
          Добавить
        </RouterLink>

</template>
