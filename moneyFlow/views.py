import json
import logging
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from moneyFlow.seriallizers import *
from moneyFlow.models import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

logger = logging.getLogger(__name__)

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