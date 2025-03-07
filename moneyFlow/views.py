from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from moneyFlow.models import Transactions, Status


# Create your views here.
class TransactionsView(View):
    def get(self, request, *args, **kwargs):
        transactions = list(Transactions.objects.all().values())
        return JsonResponse(transactions, safe=False)  # Верните просто список