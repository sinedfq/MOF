from moneyFlow.models import *
from rest_framework import viewsets

from moneyFlow.seriallizers import *

class TransactionsViewSet(viewsets.ModelViewSet):
    queryset = Transactions.objects.all()
    serializer_class = TransactionsSerializer
    def get_queryset(self):
        return Transactions.objects.all()

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
    def get_queryset(self):
        return super().get_queryset()
