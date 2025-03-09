import { method } from 'lodash';
import { defineStore } from 'pinia';

export const useTransactionsStore = defineStore('transactions', {
    state: () => ({
        transactions: [],
    }),
    actions: {
        // Фетч запрос для получения данных из таблицы
        async fetchTrans() {
            const response = await fetch('api/transitions/');
            this.transactions = await response.json();
        },
        // Фетч запрос для удаления данных из таблицы
        async delTrans(transactionsId){
            const response = await fetch(`api/transitions/${transactionsId}/`, {
                method: "DELETE"
            });
            await this.fetchTrans();      
        },
        // Фетч запрос для редактирования транзации
        async editTrans(transactionId, updatedData) {
            try {
              const response = await axios.patch(`/api/transitions/${transactionId}/`, updatedData, {
                headers: {
                  "Content-Type": "application/json",
                },
              });
          
              console.log("Данные успешно обновлены:", response.data);
          
              await this.fetchTransactions(); 
          
              return response.data;
            } catch (error) {
              console.error("Ошибка при обновлении транзакции:", error);
            }
          }
    },
});