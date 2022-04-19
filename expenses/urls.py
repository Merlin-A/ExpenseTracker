from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', views.index, name = "expenses"),
    path('add-expense', views.add_expense, name = "add_expenses"),
    path('edit-expense/<int:id>', views.expense_edit, name = "expense-edit"),
    path('delete-expense/<int:id>', views.expense_delete, name = "expense-delete"),
    path('search-expenses', csrf_exempt(views.search_expenses), name = 'search_expenses')
]
