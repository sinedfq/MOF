from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from moneyFlow.models import Transactions


# Create your views here.
class TransactionsView(View):
    def get(request, *args):
        transactions = list(Transactions.objects.all().values())
        return JsonResponse({
            "test": transactions
        })