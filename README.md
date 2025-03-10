<h1>MOF - Movement of fund </h1>

<h3>Задание: </h3>

Необходимо разработать веб-приложение, которое позволяет пользователям
создавать, редактировать, удалять и просматривать записи о движении денежных
средств. Веб-приложение должно быть удобным, иметь интуитивно понятный
интерфейс и обеспечивать соблюдение логических зависимостей между сущностями.

----

<h3>Используемые технологии: </h3>
1. Django Framework <br>
2. VueJS <br>
3. HTML/CSS <br>
4. SQLite <br>
5. Node.js

------

<h3>Инструкция по запуску: </h3>

Запуск Django проект <br>
1. Переходим в каталог MOF <br>
2. Устанавливаем требуемые компоненты <br>
```bash
  pip install -r requirements.txt
```
3. Делаем миграцию проекта
```bash
  python manage.py migrate
```
*если возникла ошибка то перед migrate выполните:
```bash
  python manage.py makemigrations
```
4. Далее запускаем наш Django проект:
```bash
  python manage.py runserver
```
![image](https://github.com/user-attachments/assets/6ebb2c1c-0e82-4d54-828b-273d804e255d)

После успешшного запуска Django-проекта перейдем к запуску VueJS проекта <br>
1. Переодим в папку client
```bash
cd client/
```
2. Для запуска требуется установить ```npm``` в случае если он не установлен
```bash
npm install
```
3. Далее запускаем проект 
```bash
npm run dev
```
![image](https://github.com/user-attachments/assets/2ed0f3c9-a747-46a0-ae4e-0f965f9a2de2)

----

<h3>Внешний вид запущенного проекта: </h3>

Главная страница(HomeView.vue)
![image](https://github.com/user-attachments/assets/afbd38d9-24b1-4d73-9cd6-64ea753c4231)
*при желании можно добавить другие поля(дата изменения, статус)

Страница редактирования транзакции(EditView.vue)
![image](https://github.com/user-attachments/assets/444105d3-dc9c-46bb-a764-a27da8ea749d)

Страница добавления транзакции/статуса/типа/категории/подкатегории (AddVuew.vue)
![image](https://github.com/user-attachments/assets/f52a77c0-0801-48a2-8afa-0c8ebcd12b74)
![image](https://github.com/user-attachments/assets/76b7ee19-4b9b-45db-a7bc-e88d41d5179d)

----

<h3>Техническое описание:</h3>

models.py
```python
class Status(models.Model):
    name = models.CharField("Status Name", unique = True, max_length=50)

    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField("Type", unique=True, max_length=155)
    
    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField("Category Name", unique= True, max_length=125)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="Type", verbose_name="Тип")
    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField("SubCategory Name", unique = True, max_length= 125)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="Category", verbose_name="Категория")

    def __str__(self):
        return self.name  
```
Определение моделей таблицы базы данных:
1. Таблица Статус(Status) имеет поля: id, name (макс. длина 50 символов)
2. Таблица Тип(Type) имеет поля: id, name (макс. длина 155 символов)
3. Таблица Категория(Category) имеет поля: id, name (макс. длина 125 символов), внешний ключ ссылнающий на класс Type
4. Таблица Подкатегория(SubCategory) имеет поля: id, name (макс. длина 125 символов), внешний ключ ссылнающий на класс Category

```python
class Transactions(models.Model):
    created_date = models.DateTimeField("Create date", auto_now_add = True)
    updated_date = models.DateField("Update date", auto_now = True)
    status = models.ForeignKey(Status, on_delete = models.PROTECT, verbose_name = "Статус")
    category = models.ForeignKey(Category, on_delete = models.SET_NULL, verbose_name = "Категория", null = True, blank = True)
    subcategory = models.ForeignKey(SubCategory, on_delete= models.SET_NULL, verbose_name = "Подкатегория", null= True, blank = True)
    type = models.ForeignKey(Type, on_delete = models.PROTECT, verbose_name = "Тип")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма", default= 0)
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    
    def clean(self):
        super().clean()
        if self.subcategory and self.category:
            if self.subcategory.category != self.category:
                raise ValidationError("Выбор подкатегории должен соответствовать выбранной категории.")

    def __str__(self):
        return f"Транзакция #{self.id} ({self.amount} руб.)"

```
5. Таблица Транзакций(Transactions) имеет поля: дата создания(created_date), дата обновления(updated_date), стоимость(amount) с дефолтным значеним 0, комментария (разрешено быть пустым),
а также остальные поля связанные внешним ключем с другими таблицами. Имеется валидация подкатегории по категории.

seriallizers.py

```python
class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'name']

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['id', 'name']


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'category']


class CategorySerializer(serializers.ModelSerializer):
    type = serializers.PrimaryKeyRelatedField(queryset=Type.objects.all())  # Доступно для записи
    subcategories = SubCategorySerializer(many=True, read_only=True)  # Только для чтения

    class Meta:
        model = Category
        fields = ['id', 'name', 'type', 'subcategories']
```

1. Сериализаторы классов Статус, Тип, Категория и Подкатегория.

```python 
class TransactionsSerializer(serializers.ModelSerializer):
    # Для чтения
    status = StatusSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    subcategory = SubCategorySerializer(read_only=True)
    type = TypeSerializer(read_only=True)

    # Для записи
    status_id = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all(), source='status', write_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)
    subcategory_id = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all(), source='subcategory', write_only=True)
    type_id = serializers.PrimaryKeyRelatedField(queryset=Type.objects.all(), source='type', write_only=True)

    class Meta:
        model = Transactions
        fields = [
            'id', 'created_date', 'updated_date', 
            'status', 'category', 'subcategory', 'type',  # Для чтения
            'status_id', 'category_id', 'subcategory_id', 'type_id',  # Для записи
            'amount', 'comment'
        ]

    def validate(self, data):
        """
        Проверка, что подкатегория соответствует категории.
        """
        if 'subcategory' in data and 'category' in data:
            if data['subcategory'].category != data['category']:
                raise serializers.ValidationError("Выбор подкатегории должен соответствовать выбранной категории.")
        return data
```
2. Сериализатор класса транзакций, который возвращает поля для чтения и поля для записи для корректной работы функций добавления/редактирования. Также тут добавлена валидация подкатегории по категории для корректной записи подкатегори к выбранной категории

views.py

```python
@method_decorator(csrf_exempt, name='dispatch')
class TransactionsView(View):
    def get(self, request, *args, **kwargs):
        try:
            transactions = Transactions.objects.all()
            serializer = TransactionsSerializer(transactions, many=True)
            return JsonResponse(serializer.data, safe=False)
        except Exception as e:
            logger.error(f"Error in TransactionsView GET: {str(e)}")
            return JsonResponse({"error": "Internal Server Error"}, status=500)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            logger.debug(f"Received data: {data}")
            serializer = TransactionsSerializer(data=data)
            if serializer.is_valid():
                transaction = serializer.save()
                return JsonResponse({"id": transaction.id, **serializer.data}, status=201)
            logger.error(f"Serializer errors: {serializer.errors}")
            return JsonResponse(serializer.errors, status=400)
        except Exception as e:
            logger.error(f"Error in TransactionsView POST: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class CategoryView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            name = data.get('name')
            type_id = data.get('type')

            if not name or not type_id:
                return JsonResponse({"error": "Name and type are required"}, status=400)

            # Проверяем, что тип существует
            try:
                type = Type.objects.get(id=type_id)
            except Type.DoesNotExist:
                return JsonResponse({"error": "Type does not exist"}, status=400)

            # Создаем новую категорию
            category = Category.objects.create(name=name, type=type)

            return JsonResponse({"id": category.id, "name": category.name, "type": category.type.id}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

class TypeView(View):
    def get(self, request, *args, **kwargs):
        try:
            types = list(Type.objects.all().values())
            return JsonResponse(types, safe=False)
        except Exception as e:
            logger.error(f"Error in TypeView GET: {str(e)}")
            return JsonResponse({"error": "Internal Server Error"}, status=500)


class StatusView(View):
    def get(self, request, *args, **kwargs):
        try:
            statuses = list(Status.objects.all().values())
            return JsonResponse(statuses, safe=False)
        except Exception as e:
            logger.error(f"Error in StatusView GET: {str(e)}")
            return JsonResponse({"error": "Internal Server Error"}, status=500)


class SubCategoryView(View):
    def get(self, request, *args, **kwargs):
        try:
            subcategories = list(SubCategory.objects.all().values())
            return JsonResponse(subcategories, safe=False)
        except Exception as e:
            logger.error(f"Error in SubCategoryView GET: {str(e)}")
            return JsonResponse({"error": "Internal Server Error"}, status=500)
```

Представления классов, для корректной отработки GET и POST запросов к базе данных. Вывод ошибки в случае если данные отправлены неверно.

api.py

```python
class TransactionsViewSet(viewsets.ModelViewSet):
    queryset = Transactions.objects.all()
    serializer_class = TransactionsSerializer

    def create(self, request, *args, **kwargs):
        print("Received data:", request.data)  # Логируем входные данные
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            print("Data is valid, saving...")
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("Validation errors:", serializer.errors)  # Логируем ошибки
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    def get_queryset(self):
        return super().get_queryset()


class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    def get_queryset(self):
        return super().get_queryset()

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    def get_queryset(self):
        return super().get_queryset()

class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

    @action(detail=False, methods=['get'], url_path='by-category/(?P<category_id>\d+)')
    def by_category(self, request, category_id=None):
        """
        Получение подкатегорий по ID категории.
        """
        try:
            # Преобразуем category_id в целое число
            category_id = int(category_id)
            # Фильтруем подкатегории по category_id
            subcategories = SubCategory.objects.filter(category_id=category_id)
            # Сериализуем данные
            serializer = self.get_serializer(subcategories, many=True)
            return Response(serializer.data)
        except ValueError:
            return Response({"error": "Invalid category_id"}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
```
Набор представлений классов. 
1. В ```TransactionsViewSet``` добавлена функция для корректного создания новой транзакции.
2. В ```SubCategoryViewSet``` добавлена функция для определения категорий, к которым причастна подкатегория.

/mof/ursl.py
```python
router = DefaultRouter()
router.register(r'transitions', TransactionsViewSet, basename= "transition" )
router.register(r'categories', CategoriesViewSet, basename= "category")
router.register(r'subcategories', SubCategoryViewSet, basename="subcategory")
router.register(r'types', TypeViewSet, basename= "type")
router.register(r'status', StatusViewSet, basename= "status")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
]
```
Добавлен ```router``` для правильного использования набора представлений и доступа к ```api```

AddTransRow.vue
```javascript
// Состояние для новой транзакции
const newTransaction = ref({
  amount: 0,
  typeId: null,
  categoryId: null,
  subcategoryId: null,
  statusId: null,
  comment: '',
});

// Списки для выбора
const types = ref([]);
const categories = ref([]);
const subcategories = ref([]);
const statuses = ref([]);

// Загрузка списков (типы, категории, статусы)
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

// Следим за изменением категории
watch(
  () => newTransaction.value.categoryId,
  (newCategoryId) => {
    if (newCategoryId) {
      fetchSubcategories(newCategoryId);
    } else {
      subcategories.value = [];
    }
  }
);

const addTransaction = async () => {
  try {
    // Проверяем, что все обязательные поля заполнены
    if (
      !newTransaction.value.amount ||
      !newTransaction.value.typeId ||
      !newTransaction.value.categoryId ||
      !newTransaction.value.statusId
    ) {
      alert('Пожалуйста, заполните все обязательные поля.');
      return;
    }

    // Подготовка данных для отправки
    const payload = {
      status_id: newTransaction.value.statusId,  
      category_id: newTransaction.value.categoryId,  
      subcategory_id: newTransaction.value.subcategoryId,  
      type_id: newTransaction.value.typeId,  
      amount: newTransaction.value.amount,
      comment: newTransaction.value.comment,
    };


    // Отправка данных на сервер с использованием fetch
    const response = await fetch('/api/transitions/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(`Ошибка сервера: ${response.status} - ${JSON.stringify(errorData)}`);
    }

    const responseData = await response.json();
    console.log('Транзакция успешно добавлена:', responseData);

    // Сброс формы
    newTransaction.value = {
      amount: 0,
      typeId: null,
      categoryId: null,
      subcategoryId: null,
      statusId: null,
      comment: '',
    };

    alert('Транзакция успешно добавлена!');
  } catch (error) {
    console.error('Ошибка при добавлении транзакции:', error);
    alert('Не удалось добавить транзакцию. Пожалуйста, попробуйте снова.');
  }
};
```
Основной функционал добавления новых транзакций в таблицу базы данных. <br>
Сначала мы создаём новый набор даннах, который при помощи ```POST``` запроса мы будет отправлять в нашу базу данных. <br> <br>
При помощи ```axios``` запросов мы получаем все поля, которые привязаны к модели Transactions внешним ключём (Category, Status, Type, SubCategory). 
Далее мы получаем Подкатегории к выбранной Категории (отслеживаем выбор категории при помощи метода ```watch``` <br> <br>
После заполнения всех полей в ```template``` мы вызываем функцию ```addTransaction```, в которую мы передаём заполненную информацию и функция выполняет ```fetch - POST``` запрос в нашу БД <br><br>

CategoryRov.vue
```javascript
// Состояние для новой категории
const newCategory = ref({
  name: '',
  typeId: null,
});

// Состояние для редактируемой категории
const editCategory = ref({
  id: null,
  name: '',
  typeId: null,
});

// Список типов для выбора
const types = ref([]);

// Список категорий
const categories = ref([]);

// Загрузка списка типов
const fetchTypes = async () => {
  try {
    const response = await axios.get('/api/types/');
    types.value = response.data;
  } catch (error) {
    console.error('Ошибка при загрузке типов:', error);
  }
};

// Загрузка списка категорий
const fetchCategories = async () => {
  try {
    const response = await axios.get('/api/categories/');
    categories.value = response.data.map(category => {
      // Находим тип по ID
      const type = types.value.find(t => t.id === category.type);
      return {
        ...category,
        typeName: type ? type.name : 'Тип не найден', // Добавляем имя типа
      };
    });
    console.log('Категории загружены:', categories.value); // Логируем данные
  } catch (error) {
    console.error('Ошибка при загрузке категорий:', error);
  }
};

// Функция для добавления новой категории
const addCategory = async () => {
  try {
    if (!newCategory.value.typeId) {
      alert('Пожалуйста, выберите тип.');
      return;
    }

    const payload = {
      name: newCategory.value.name,
      type: newCategory.value.typeId,
    };

    const response = await axios.post('/api/categories/', payload, {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    console.log('Категория успешно добавлена:', response.data);

    newCategory.value = {
      name: '',
      typeId: null,
    };

    alert('Категория успешно добавлена!');
    fetchCategories(); // Обновляем список категорий
  } catch (error) {
    console.error('Ошибка при добавлении категории:', error);
    alert('Не удалось добавить категорию. Пожалуйста, попробуйте снова.');
  }
};

// Функция для начала редактирования категории
const startEdit = (category) => {
  editCategory.value = {
    id: category.id,
    name: category.name,
    typeId: category.type, // Используем ID типа
  };
};

// Функция для сохранения изменений категории
const saveEdit = async () => {
  try {
    const payload = {
      name: editCategory.value.name,
      type: editCategory.value.typeId,
    };

    const response = await axios.put(`/api/categories/${editCategory.value.id}/`, payload, {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    console.log('Категория успешно обновлена:', response.data);

    editCategory.value = {
      id: null,
      name: '',
      typeId: null,
    };

    alert('Категория успешно обновлена!');
    fetchCategories(); // Обновляем список категорий
  } catch (error) {
    console.error('Ошибка при обновлении категории:', error);
    alert('Не удалось обновить категорию. Пожалуйста, попробуйте снова.');
  }
};

// Функция для отмены редактирования
const cancelEdit = () => {
  editCategory.value = {
    id: null,
    name: '',
    typeId: null,
  };
};

// Загружаем типы и категории при монтировании компонента
onMounted(async () => {
  await fetchTypes(); // Сначала загружаем типы
  await fetchCategories(); // Затем загружаем категории
});
```
Данный участок кода реализует добавление и редактирование полей в модели Category<br><br>
Аналогично с ```AddTransRow.vue``` мы получаем, необходимую для этого поля, набор данных, с которым мы и продолжим работу. <br><br>
Однако в ```AddTransRow.vue``` для добавления новой транзакции мы использовали ```fetch``` тут же мы используем ```axios``` запросы для удобства. <br><br>
Редактирование происходит посредством выбора категории и заполнения необходимых полей(name, type), далее после нажатия на кнопку "Сохранить" вызывается функция ```saveEdit```, которая, 
получив необходимые данный, делает ```axios.put``` запрос к БД. <br><br>
Аналогично происходит и в остальных компонентах (```StatusRow.vue, SubCategoryRow.vue, TypeRov.vue```) Front-end части проекта 
<br><br>

TransRow.vue
```javascript
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
```
В данном учатске кода происходит отрисовка и распределения объектов из базы данных посредством цикла ```<li v-for="transaction in sortedTransactions" :key="transaction.id">```, 
необходимы для этого данные мы передали, через ```HomeVie.vue```
```html
    <TransRow 
        :sortedTransactions="sortedTransactions" 
```
Данные в ```sortedTransactions``` мы получили из функции используя ```fetch``` запрос
```javascript
        async fetchTrans() {
            const response = await fetch('api/transitions/');
            this.transactions = await response.json();
        },
```
Удаление транзакции происходит также через ```fetch``` запрос
```javascript
        async delTrans(transactionsId){
            const response = await fetch(`api/transitions/${transactionsId}/`, {
                method: "DELETE"
            });
            await this.fetchTrans();      
        },
```
<br><br>
Чтобы ```POST``` и ```GET``` запросы к другому порту работали корректно и не выдавали ошибку было добавлено прокси, которое перенаправляет запросы с указанием ```/api``` на другой порт
```javascript
// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    proxy: {
      "/api": "http://127.0.0.1:8000/"
    }
  }
})
```
