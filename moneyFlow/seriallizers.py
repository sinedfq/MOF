from rest_framework import serializers
from .models import *

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['name'] 

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['name']

class TransactionsSerializer(serializers.ModelSerializer):
    status = StatusSerializer()
    type = TypeSerializer()
    category = CategorySerializer()
    subcategory = SubCategorySerializer()
    class Meta:
        model = Transactions
        fields = '__all__'