from django.urls import path
from moneyFlow.views import TransactionsView


urlpatterns = [
    path('transactions/', TransactionsView.as_view()),    
]
