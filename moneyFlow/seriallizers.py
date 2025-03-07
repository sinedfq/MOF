from rest_framework import serializers
from .models import Status, Type, Category, SubCategory, Transactions

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'name']

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['id', 'name']

class CategorySerializer(serializers.ModelSerializer):
    type = TypeSerializer(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'type']

class SubCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'category']

class TransactionsSerializer(serializers.ModelSerializer):
    status = StatusSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    subcategory = SubCategorySerializer(read_only=True)
    type = TypeSerializer(read_only=True)

    class Meta:
        model = Transactions
        fields = ['id', 'created_date', 'updated_date', 'status', 'category', 'subcategory', 'type', 'amount', 'comment']

    def validate(self, data):
        """
        Проверка, что подкатегория соответствует категории.
        """
        if 'subcategory' in data and 'category' in data:
            if data['subcategory'].category != data['category']:
                raise serializers.ValidationError("Выбор подкатегории должен соответствовать выбранной категории.")
        return data