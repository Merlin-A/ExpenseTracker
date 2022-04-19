from django.contrib import admin
from django.db import models
from .models import Expense, Category
# Register your models here.

class ExpenseAdmin(admin.ModelAdmin):
    
    list_display = ('category', 'amount', 'date', 'owner' )
    list_per_page = 5



admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Category)
