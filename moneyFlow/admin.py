from django.contrib import admin
from moneyFlow.models import *

# Register your models here.

@admin.register(Transactions)
class AuthorAdmin(admin.ModelAdmin):
    pass

@admin.register(SubCategory)
class AuthorAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class AuthorAdmin(admin.ModelAdmin):
    pass

@admin.register(Type)
class AuthorAdmin(admin.ModelAdmin):
    pass

@admin.register(Status)
class AuthorAdmin(admin.ModelAdmin):
    pass