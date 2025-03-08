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


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'category']


class CategorySerializer(serializers.ModelSerializer):
    type = serializers.PrimaryKeyRelatedField(queryset=Type.objects.all())  # Доступно для записи
    subcategories = SubCategorySerializer(many=True, read_only=True)  # Только для чтения

    class Meta:
        model = Category
        fields = ['id', 'name', 'type', 'subcategories']

class TransactionsSerializer(serializers.ModelSerializer):
    status = StatusSerializer()
    category = CategorySerializer()
    subcategory = SubCategorySerializer()
    type = TypeSerializer()

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