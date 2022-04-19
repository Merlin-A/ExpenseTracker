from concurrent.futures import thread
import email
from lib2to3.pgen2 import token
from django.shortcuts import redirect, render
from django.views import View
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib import auth
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_generator
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
import threading
# Create your views here.


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)

class EmailValidationView(View):
    def post(self, request):
        # Requests the input data from the body
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is Invalid'}, status=400)

        elif User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':   'Email already registered choose another One'}, status=409)

        return JsonResponse({'email_valid': True})


class UsernameValidationView(View):
    def post(self, request):
        # Requests the input data from the body
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric charachters'}, status=400)

        elif User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':   'Username in use choose another One'}, status=409)

        return JsonResponse({'username_valid': True})


class RegistrationView(View):
    def get(self, request):  # this is the initial page request which shows us the page
        return render(request, 'authentication/register.html')

    def post(self, request):

        # TO REGISTER A USER
        # GET USER DATA
        # VALIDATE USER
        # CREATE USER ACCNT

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # TO KEEP THE VALUE EVEN AFTER MESSAGE

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password too Short')
                    return render(request, 'authentication/register.html', context)

                if len(password) > 36:
                    messages.error(request, 'Password too Long')
                    return render(request, 'authentication/register.html', context)

                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()

                # path_to_view
                # --Domain we aer on
                # relative url to verification
                # encode ui

                # Primary Key unique for each entry in the database
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={
                               'uidb64': uidb64, 'token': token_generator.make_token(user)})
                activate_url = 'http://'+domain+link
                email_subject = 'Activate your Account'
                email_body = 'Hi '+user.username + \
                    ' Please use this link to verify your account\n' + activate_url
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@test.com',
                    [email],

                )

                EmailThread(email).start()
                
                messages.success(request, 'Account Created Succesfully')
                return render(request, 'authentication/register.html')

        return render(request, 'authentication/register.html')


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                return redirect('login' + messages.warning(request, 'Sorry ' + user.username + " Account Already Activated"))

            if user.is_active:
                return redirect('login')

            user.is_active = True
            user.save()

            messages.success(request, 'Account Activated Successfully')

        except Exception as e:
            pass

        return redirect('login')


class LoginView(View):
    def get(self, request):

        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome ' +
                                     user.username + ' You are now logged in')
                    return redirect('expenses')

                elif not user.is_active:
                    messages.error(
                        request, 'Account is not activated, please check email')
                    return render(request, 'authentication/login.html')

            elif not user:
                messages.error(
                    request, 'Invalid Credentials, Please Try Again')
                return render(request, 'authentication/login.html')

        else:
            messages.error(request, 'Please fill all fields, try again')
            return render(request, 'authentication/login.html')


class LogoutView(View):
    def post(self, request):

        auth.logout(request)
        messages.success(request, ' You Logged Out Succesfully')
        return redirect('login')


class RequestPasswordResetEmail(View):
    def get(self, request):

        return render(request, 'authentication/reset-password.html')

    def post(self, request):

        email = request.POST['email']
        context = {
            'values': request.POST
        }

        if not User.objects.filter(email=email):
            messages.error(request, 'Uregistered Email')
            return render(request, 'authentication/reset-password.html', context)

        # else:
        #     messages.info(request, 'Email is Registered')
        user = User.objects.filter(email=email)

        if user.exists():

            uidb64 = urlsafe_base64_encode(force_bytes(user[0].pk))
            domain = get_current_site(request).domain
            link = reverse(
                'reset-user-password', kwargs={
                    'uidb64': uidb64,
                    'token': PasswordResetTokenGenerator().make_token(user[0])}
            )

            reset_url = 'http://'+domain+link
            email_subject = 'Password Reset Email Instructions '
            email_body = '\n Hi there,' + \
                ' Please use this link to Reset your password\n' + reset_url
            space = '\n'
            email = EmailMessage(
                email_subject,
                email_body,
                'noreply@test.com',
                [email],

            )

            EmailThread(email).start()
            

        messages.success(request, 'We have sent you an email')

        return render(request, 'authentication/reset-password.html')


class CompletePasswordReset(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token,

        }

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):

                messages.warning(request, 'Password Link Invalid')
                return render(request, 'authentication/reset-password.html')

        except:

            pass
        return render(request, 'authentication/set-new-password.html', context)

    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token,

        }

        password = request.POST['password']
        password1 = request.POST['password1']

        if password != password1:
            messages.error(request, 'Different Passwords')
            return render(request, 'authentication/set-new-password.html', context)

        elif len(password) < 6 or len(password) > 30:
            messages.error(request, "Password should have 6 - 30 charachters")
            return render(request, 'authentication/set-new-password.html', context)

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)

            user.set_password(password)
            user.save()

            messages.success(request, 'New Password Saved')
            return redirect('login')

        except:

            messages.info(request, 'Something Went Wrong, Try Again')
            return render(request, 'authentication/set-new-password.html', context)
