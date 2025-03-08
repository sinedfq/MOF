from django.urls import path
from moneyFlow.views import *


urlpatterns = [
    path('transactions/', TransactionsView.as_view()),
    path('categories/', CategoryView.as_view()),
    path('type/', TypeView.as_view()),
    path('status/', StatusView.as_view()),
    path('subcategory/', SubCategoryView.as_view())
]
