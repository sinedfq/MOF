import { defineStore } from 'pinia';

export const useTransactionsStore = defineStore('transactions', {
    state: () => ({
        transactions: [],
    }),
    actions: {
        async fetchTrans() {
            const response = await fetch('/api/MOF/transactions'); // Измените URL на ваш
            this.transactions = await response.json();
        },
    },
});