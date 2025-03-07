import { method } from 'lodash';
import { defineStore } from 'pinia';

export const useTransactionsStore = defineStore('transactions', {
    state: () => ({
        transactions: [],
    }),
    actions: {
        async fetchTrans() {
            const response = await fetch('api/transitions/'); // Измените URL на ваш
            this.transactions = await response.json();
        },
        async delTrans(transactionsId){
            const response = await fetch(`api/transitions/${transactionsId}/`, {
                method: "DELETE"
            });
            await this.fetchTrans();      
        }
    },
});