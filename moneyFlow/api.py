from moneyFlow.models import *
from rest_framework import viewsets

from moneyFlow.seriallizers import TransactionsSerializer

class TransactionsViewSet(viewsets.ModelViewSet):
    queryset = Transactions.objects.all()
    serializer_class = TransactionsSerializer
    def get_queryset(self):
        return Transactions.objects.all()