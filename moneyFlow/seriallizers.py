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
    # Для чтения
    status = StatusSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    subcategory = SubCategorySerializer(read_only=True)
    type = TypeSerializer(read_only=True)

    # Для записи
    status_id = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all(), source='status', write_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)
    subcategory_id = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all(), source='subcategory', write_only=True)
    type_id = serializers.PrimaryKeyRelatedField(queryset=Type.objects.all(), source='type', write_only=True)

    class Meta:
        model = Transactions
        fields = [
            'id', 'created_date', 'updated_date', 
            'status', 'category', 'subcategory', 'type',  # Для чтения
            'status_id', 'category_id', 'subcategory_id', 'type_id',  # Для записи
            'amount', 'comment'
        ]

    def validate(self, data):
        """
        Проверка, что подкатегория соответствует категории.
        """
        if 'subcategory' in data and 'category' in data:
            if data['subcategory'].category != data['category']:
                raise serializers.ValidationError("Выбор подкатегории должен соответствовать выбранной категории.")
        return data