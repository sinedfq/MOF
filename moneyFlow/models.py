from django.db import models
from django.forms import ValidationError

class Status(models.Model):
    name = models.CharField("Status Name", unique = True, max_length=50)

    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField("Type", unique=True, max_length=155)
    
    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField("Category Name", unique= True, max_length=125)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="Type", verbose_name="Тип")
    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField("SubCategory Name", unique = True, max_length= 125)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="Category", verbose_name="Категория")

    def __str__(self):
        return self.name  


class Transactions(models.Model):
    created_date = models.DateTimeField("Create date", auto_now_add = True)
    updated_date = models.DateField("Update date", auto_now = True)
    status = models.ForeignKey(Status, on_delete = models.PROTECT, verbose_name = "Статус")
    category = models.ForeignKey(Category, on_delete = models.SET_NULL, verbose_name = "Категория", null = True, blank = True)
    subcategory = models.ForeignKey(SubCategory, on_delete= models.SET_NULL, verbose_name = "Подкатегория", null= True, blank = True)
    type = models.ForeignKey(Type, on_delete = models.PROTECT, verbose_name = "Тип")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма", default= 0)
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    
    def clean(self):
        super().clean()
        if self.subcategory and self.category:
            if self.subcategory.category != self.category:
                raise ValidationError("Выбор подкатегории должен соответствовать выбранной категории.")

    def __str__(self):
        return f"Транзакция #{self.id} ({self.amount} руб.)"

