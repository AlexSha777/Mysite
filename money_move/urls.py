from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('income/', views.income_view, name='income'),
    path('income/success_add', views.income_success_add, name='success_add'),
    path('spendings/', views.spendings_view, name='spendings'),
    path('spendings/success_add', views.spending_success_add, name='success_add'),
    path('income/add_new_source', views.add_new_source, name='add_new_source'),
    path('spendings/add_new_spending_kind', views.add_new_spending_kind, name='add_new_spending_kind'),
    path('cash/', views.cash_view, name='cash'),
    path('cash/success_add', views.cash_success_add, name='success_add'),
    path('cash/add_new_cashkind', views.add_new_cashkind, name='add_new_cashkind'),
    path('analysing/', views.analysing, name='analysing'),
    path('analysing/sending_excel', views.sending_excel, name='sending_excel'),
]