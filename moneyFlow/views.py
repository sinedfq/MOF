from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from moneyFlow.models import *


class TransactionsView(View):
    def get(self, request, *args, **kwargs):
        transactions = list(Transactions.objects.all().values())
        return JsonResponse(transactions, safe=False)

class CategoryView(View):
    def get(self, request, *args, **kwargs):
        category = list(Category.objects.all().values())
        return JsonResponse(category, safe=False) 
    
    
class TypeView(View):
    def get(self, request, *args, **kwargs):
        type = list(Type.objects.all().values)
        return JsonResponse(type, safe=False)

class StatusView(View):
    def get(self, request, *args, **kwargs):
        status = list(Type.objects.all().values)
        return JsonResponse(status, safe=False)
    
class SubCategoryView(View):
    def get(self, request, *args, **kwargs):
        subcategory = list(SubCategory.objects.all().values)
        return JsonResponse(subcategory, safe=False)