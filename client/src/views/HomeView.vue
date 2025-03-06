<script setup>
import { onBeforeMount } from 'vue';
import { useTransactionsStore } from '../stores/tranc';
import __ from 'lodash'

const transStore = useTransactionsStore();

onBeforeMount(async () => {
    await transStore.fetchTrans(); // Не забывайте использовать await
});
</script>

<template>
    <h1>Главная страница</h1>
    <ul>
        <li v-for="transaction in transStore.transactions" :key="transaction.id">
            {{ transaction }}
        </li>

    </ul>
</template>
