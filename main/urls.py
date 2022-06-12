from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('<str:symbol>/income', views.income, name="income"),
    path('companies/', views.companies, name="companies"),
    path('company/<str:pk>/', views.company, name="company"),
    path('financials/<str:pk>/', views.financials, name="financials"),
]
