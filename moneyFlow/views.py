from rest_framework.views import APIView
from rest_framework.response import Response
from moneyFlow.models import Transactions, Status
from moneyFlow.seriallizers import TransactionsSerializer

class TransactionsView(APIView):
    def get(self, request):
        transactions = Transactions.objects.all()  # Получаем все транзакции
        serializer = TransactionsSerializer(transactions, many=True)
        return Response(serializer.data)