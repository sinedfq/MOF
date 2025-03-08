from moneyFlow.models import *
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from moneyFlow.seriallizers import *
from rest_framework import status

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