from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', views.index, name = "expenses"),
    path('add-expense', views.add_expense, name = "add_expenses"),
    path('edit-expense/<int:id>', views.expense_edit, name = "expense-edit"),
    path('delete-expense/<int:id>', views.expense_delete, name = "expense-delete"),
    path('search-expenses', csrf_exempt(views.search_expenses), name = 'search_expenses'),
    path('expense_category_summary', views.expense_category_summary, name = 'expense_category_summary'),
    path('stats', views.statsView, name = 'stats'),
    path('export-csv', views.export_csv, name = 'export-csv'),
    path('export-xls', views.export_xls, name = 'export-xls'),
    # path('export-pdf', views.export_pdf, name = 'export-pdf'),






]
