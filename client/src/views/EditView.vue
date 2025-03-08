<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const transactionId = route.params.transactionId;

// Состояние для данных транзакции
const transaction = ref({
  amount: 0,
  type: null,
  category: null,
  subcategory: null,
  status: null,
  comment: '',
});

// Списки для выбора
const types = ref([]);
const categories = ref([]);
const subcategories = ref([]);
const statuses = ref([]);

// Загрузка данных транзакции
const fetchTransaction = async () => {
  try {
    console.log('Fetching transaction from:', `/api/transitions/${transactionId}/`);
    const response = await axios.get(`/api/transitions/${transactionId}/`);
    transaction.value = response.data;
  } catch (error) {
    console.error('Ошибка при загрузке транзакции:', error);
  }
};
// Загрузка списков (типы, категории, подкатегории, статусы)
const fetchInitialData = async () => {
  try {
    const [typesResponse, categoriesResponse, statusesResponse] = await Promise.all([
      axios.get('/api/types/'),
      axios.get('/api/categories/'),
      axios.get('/api/status/'),
    ]);
    types.value = typesResponse.data;
    categories.value = categoriesResponse.data;
    statuses.value = statusesResponse.data;
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
};

// Загрузка подкатегорий по выбранной категории
const fetchSubcategories = async (categoryId) => {
  if (!categoryId) {
    subcategories.value = [];
    return;
  }
  try {
    const response = await axios.get(`/api/subcategories/by-category/${categoryId}/`);
    subcategories.value = response.data;
  } catch (error) {
    console.error('Ошибка при загрузке подкатегорий:', error);
  }
};
// Валидация подкатегории по категории
const validateSubcategory = () => {
  if (
    transaction.value.subcategory &&
    transaction.value.category &&
    transaction.value.subcategory.category !== transaction.value.category.id
  ) {
    alert('Выбранная подкатегория не соответствует категории.');
    transaction.value.subcategory = null; // Сбросить подкатегорию
  }
};

// Следим за изменением категории
watch(
  () => transaction.value.category,
  (newCategory) => {
    if (newCategory) {
      fetchSubcategories(newCategory.id);
    } else {
      subcategories.value = [];
    }
    validateSubcategory();
  }
);

// Сохранение изменений
const saveTransaction = async () => {
  try {
    const payload = {
      ...transaction.value,
      type: transaction.type?.id,
      category: transaction.category?.id,
      subcategory: transaction.subcategory?.id,
      status: transaction.status?.id,
    };
    await axios.patch(`/api/transitions/${transactionId}/`, payload);
    alert('Транзакция успешно обновлена!');
  } catch (error) {
    console.error('Ошибка при обновлении транзакции:', error);
    alert('Не удалось обновить транзакцию. Пожалуйста, попробуйте снова.');
  }
};

// Загружаем данные при монтировании компонента
onMounted(async () => {
  await fetchInitialData();
  await fetchTransaction();
  if (transaction.value.category) {
    await fetchSubcategories(transaction.value.category.id);
  }
});
</script>

<template>
  <div>
    <label>Редактирование транзакции #{{ transactionId }}</label>
    <div>
      <label for="amount">Сумма:</label>
      <input
        style="width: 89%;"
        id="amount"
        v-model.number="transaction.amount"
        type="number"
        step="0.01"
        placeholder="Введите сумму"
      />
    </div>

    <!-- Поле для типа -->
    <div>
      <label for="type">Тип:</label>
      <select id="type" v-model="transaction.type">
        <option v-for="type in types" :key="type.id" :value="type">
          {{ type.name }}
        </option>
      </select>
    </div>

    <!-- Поле для категории -->
    <div>
      <label for="category">Категория:</label>
      <select id="category" v-model="transaction.category">
        <option v-for="category in categories" :key="category.id" :value="category">
          {{ category.name }}
        </option>
      </select>
    </div>

    <!-- Поле для подкатегории -->
    <div>
      <label for="subcategory">Подкатегория:</label>
      <select id="subcategory" v-model="transaction.subcategory">
        <option v-for="subcategory in subcategories" :key="subcategory.id" :value="subcategory">
          {{ subcategory.name }}
        </option>
      </select>
    </div>

    <!-- Поле для статуса -->
    <div>
      <label for="status">Статус:</label>
      <select id="status" v-model="transaction.status">
        <option v-for="status in statuses" :key="status.id" :value="status">
          {{ status.name }}
        </option>
      </select>
    </div>

    <!-- Поле для комментария -->
    <div>
      <label for="comment">Комментарий:</label>
      <textarea
        id="comment"
        v-model="transaction.comment"
        placeholder="Введите комментарий"
      ></textarea>
    </div>

    <!-- Кнопка для сохранения -->
    <button class = "custom-button" style="margin-left: 90%;" @click="saveTransaction">Сохранить</button>
  </div>
</template>

<style scoped>
div {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  text-align: center;
  font-family: 'Quicksand', sans-serif;
  font-size: 19px;
  letter-spacing: 4px;
  word-spacing: 1px;
  color: #8c8c8c;
  font-weight: normal;
  text-decoration: none;
  font-style: normal;
  font-variant: normal;
  text-transform: uppercase;
}

input,
select,
textarea {
  max-width: 100%;
  margin-left: 5%;
  align-content: center;
  width: 90%;
  padding: 0.5rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-shadow: 0px 4px 8px 0px rgba(0,0,0,0.2);
  animation: myAnim 0.5s ease-in;
}

@keyframes myAnim {
	0% {
    margin-top: -5px;
    scale: 0;
		opacity: 0;
	}
	100% {
    margin-top: 0px;
    scale: 1;
		opacity: 1;
	}
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