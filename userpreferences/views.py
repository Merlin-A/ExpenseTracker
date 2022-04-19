from django.shortcuts import render
import os
import json
from django.conf import settings
from .models import UserPreference
from django.contrib import messages
# Create your views here.


def index(request):
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for k, v in data.items():
            currency_data.append({'name': k, 'value': v})

    # checks if userprefrence already present
    exists = UserPreference.objects.filter(user=request.user).exists()
    user_preferences = None
    if exists:
        user_preferences = UserPreference.objects.get(
            user=request.user)  # is exists get
    if request.method == 'GET':

        return render(request, 'preferences/index.html', {'currencies': currency_data,  # returns userpreference throught the get request render
                                                          'user_preferences': user_preferences})
    else:

        currency = request.POST['currency']
        if exists:
            # if exists we need to show it on the site, thus the post request
            user_preferences.currency = currency
            user_preferences.save()  # save the user preference
        else:
            # if doesn't exists create(user, preferecne)
            UserPreference.objects.create(user=request.user, currency=currency)
        messages.success(request, 'Changes saved')
        return render(request, 'preferences/index.html', {'currencies': currency_data, 'user_preferences': user_preferences})
