import pdb
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from matplotlib.style import context
from django.contrib import messages
from tomlkit import date
from .models import Source, UserIncome
import json
from django.core.paginator import Paginator
from django.http import JsonResponse
from userpreferences.models import UserPreference
from datetime import time

# Create your views here.


def search_income(request):
    if request.method == 'POST':
        
        search_str = json.loads(request.body).get('searchText')
        userincome = UserIncome.objects.filter(amount__istartswith = search_str, owner = request.user) | UserIncome.objects.filter(
            date__istartswith = search_str, owner = request.user) | UserIncome.objects.filter(
            description__icontains = search_str, owner = request.user) | UserIncome.objects.filter(
            source__icontains = search_str, owner = request.user)

        data = userincome.values()


        return JsonResponse(list(data), safe = False)

@login_required(login_url='/authentication/login')
def index(request):
    sources = Source.objects.all()
    income = UserIncome.objects.all()

    userincome = UserIncome.objects.filter(owner = request.user)

    paginator = Paginator(userincome, 4)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator,page_number)
    currency = UserPreference.objects.get(user = request.user).currency
    currency1 = currency[0:3]
    
    context = {
        'userincome': userincome,
        'page_obj': page_obj,
        'currency': currency1,
    }


    return render(request, 'userincome/index.html', context) 


@login_required(login_url='/authentication/login')
def add_income(request):
    sources = Source.objects.all()
    context = {

        'sources': sources,
        'values': request.POST
        
    }
    if request.method == 'GET':
       

        return render(request, 'userincome/add_income.html', context)

    


    if request.method == 'POST':
        
        amount = request.POST['amount']
        description = request.POST['description']
        source = request.POST['source']
        date = request.POST['date']

      
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'userincome/add_income.html', context)


   
                     
            
        # if not description:
        #     messages.error(request, 'Description is required')
        #     return render(request, 'userincome/add_income.html', context)



        elif (source == 'Choose....') or (not source):
            messages.error(request, 'Income Source is required')
            return render(request, 'userincome/add_income.html', context)

        elif not date:
            messages.error(request, 'Date is required')
            return render(request, 'userincome/add_income.html', context)


        

       
        UserIncome.objects.create(owner = request.user, amount = amount, date = date, source = source, description = description)
        

        messages.success(request, 'Saved Succesfully')
        return redirect('income')


def income_edit(request, id):
    income = UserIncome.objects.get(pk = id) #to get the user details and get that speicific detail sheet
    userincome = Source.objects.all()

    context = {
        'income': income,
        'values': income,
        'userincome': userincome
    }

    if request.method == 'GET':

        return render(request, 'userincome/edit_income.html', context)
        

    
    if request.method == 'POST':
        
        amount = request.POST['amount']
        description = request.POST['description']
        income = request.POST['income']
        date = request.POST['date']

    
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'userincome/edit_income.html', context)



                    
            
        # if not description:
        #     messages.error(request, 'Description is required')
        #     return render(request, 'userincome/add_income.html', context)



        elif (income == 'Choose....') or (not income):
            messages.error(request, 'income is required')
            return render(request, 'userincome/edit_income.html', context)

        elif not date:
            messages.error(request, 'Date is required')
            return render(request, 'userincome/edit_income.html', context)


        

    
        income.owner = request.user
        income.amount = amount
        income.date = date
        income.income = income
        income.description = description
        income.save()

        messages.success(request, 'Income updated succesfully')
        
        
        return redirect('income')




    else:
        messages.info(request, 'Handling post form')
        return render(request, 'userincome/edit-income.html', context)


def income_delete(request, id):
    income = UserIncome.objects.get(pk = id)
    income.delete()
    messages.success(request, 'Income Deleted Succesfully')
    return redirect('income')