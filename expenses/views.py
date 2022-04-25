from asyncore import write
import pdb
from urllib import response
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from matplotlib.style import context
from django.contrib import messages
from tomlkit import date, datetime
from expenses.models import Category
from .models import Category, Expense
import json
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from userpreferences.models import UserPreference
import datetime
import csv
# Create your views here.


def search_expenses(request):
    if request.method == 'POST':
        
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(amount__istartswith = search_str, owner = request.user) | Expense.objects.filter(
            date__istartswith = search_str, owner = request.user) | Expense.objects.filter(
            description__icontains = search_str, owner = request.user) | Expense.objects.filter(
            category__icontains = search_str, owner = request.user)

        data = expenses.values()


        return JsonResponse(list(data), safe = False)

@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    expense = Expense.objects.all()

    expenses = Expense.objects.filter(owner = request.user)

    paginator = Paginator(expenses, 4)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator,page_number)

    try:
        currency = UserPreference.objects.get(user = request.user).currency

    except UserPreference.DoesNotExist:
        currency = 'INR - Indian Rupee'

    currency1 = currency[0:3]
    
    
    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency1,
    }


    return render(request, 'expenses/index.html', context) 


def add_expense(request):
    categories = Category.objects.all()
    todays_date = datetime.date.today()

    context = {

        'categories': categories,
        'values': request.POST,
        'today': todays_date        
    }
    if request.method == 'GET':
       

        return render(request, 'expenses/add_expense.html', context)

    


    if request.method == 'POST':
        
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['date']

      
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', context)


   
                     
            
        # if not description:
        #     messages.error(request, 'Description is required')
        #     return render(request, 'expenses/add_expense.html', context)



        elif (category == 'Choose....') or (not category):
            messages.error(request, 'Category is required')
            return render(request, 'expenses/add_expense.html', context)

        elif not date:
            messages.error(request, 'Date is required')
            return render(request, 'expenses/add_expense.html', context)


        

       
        Expense.objects.create(owner = request.user, amount = amount, date = date, category = category, description = description)
        

        messages.success(request, 'Saved Succesfully')
        return redirect('expenses')




def expense_edit(request, id):
    expense = Expense.objects.get(pk = id) #to get the user details and get that speicific detail sheet
    categories = Category.objects.all()

    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }

    if request.method == 'GET':

        return render(request, 'expenses/edit-expense.html', context)
        

    
    if request.method == 'POST':
        
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['date']

    
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit-expense.html', context)



                    
            
        # if not description:
        #     messages.error(request, 'Description is required')
        #     return render(request, 'expenses/add_expense.html', context)



        elif (category == 'Choose....') or (not category):
            messages.error(request, 'Category is required')
            return render(request, 'expenses/edit-expense.html', context)

        elif not date:
            messages.error(request, 'Date is required')
            return render(request, 'expenses/edit-expense.html', context)


        

    
        expense.owner = request.user
        expense.amount = amount
        expense.date = date
        expense.category = category
        expense.description = description
        expense.save()

        messages.success(request, 'Expense updated succesfully')
        
        
        return redirect('expenses')




    else:
        messages.info(request, 'Handling post form')
        return render(request, 'expenses/edit-expense.html', context)


def expense_delete(request, id):
    expense = Expense.objects.get(pk = id)
    expense.delete()
    messages.success(request, 'Expense Deleted Succesfully')
    return redirect('expenses')



def expense_category_summary(request):

    todays_date = datetime.date.today()
    six_months_ago = todays_date - datetime.timedelta(180)
    expenses = Expense.objects.filter(owner = request.user, date__gte = six_months_ago, date__lte = todays_date)
    finalrep = {}

    def get_category(expense):
        return expense.category

    
    category_list = list(set(map(get_category, expenses))) #set so all the categories even teh duplicate ones are listed 

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category = category)

        for item in filtered_by_category:
            amount += item.amount 
        return amount

    for x in expenses:
        for y in category_list:

            finalrep[y] = get_expense_category_amount(y)
    
    return JsonResponse({'expense_category_data': finalrep}, safe = False)




def statsView(request):
    return render(request, 'expenses/stats.html')



def export_csv(request):
    response = HttpResponse(content_type = 'text/csv') 
    response['Content-Disposition'] = 'attachment; filename = Expenses ' + str(datetime.date.today()) +".csv"

    writer = csv.writer(response)
    writer.writerow(['Amount', 'Description', 'Category', 'Date'])

    expenses = Expense.objects.filter(owner = request.user)

    for expense in expenses:

        writer.writerow([expense.amount, expense.description, expense.category, expense.date])
    

    return response