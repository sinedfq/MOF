from django.db import models

class Status(models.Model):
    status_name = models.CharField("Status Name", unique = True, max_length=50)

    def __str__(self):
        return self.name

class Type(models.Model):
    type_name = models.CharField("Type", unique=True, max_length=155)
    
    def __str__(self):
        return self.name
    
class Category(models.Model):
    categort_name = models.CharField("Category Name", unique= True, max_length=125)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    subcategory_name = models.CharField("SubCategory Name", unique = True, max_length= 125)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories", verbose_name="Категория")

    def __str__(self):
        return self.name  

# Create your models here.
class Transactions(models.Model):
    created_date = models.DateTimeField("Create date", auto_now_add = True)
    updated_date = models.DateField("Update date", auto_now = True)
    status = models.ForeignKey(Status, on_delete = models.PROTECT, verbose_name = "Статус")
    category = models.ForeignKey(Category, on_delete = models.SET_NULL, verbose_name = "Категория", null = True, blank = True)
    subcategory = models.ForeignKey(SubCategory, on_delete= models.SET_NULL, verbose_name = "Подкатегория", null= True, blank = True)
    type = models.ForeignKey(Type, on_delete = models.PROTECT, verbose_name = "Тип")
    
    def __str__(self):
        return f"Транзакция #{self.id} ({self.amount} руб.)"

