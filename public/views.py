from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

class LoginPageView(TemplateView):
    template_name = "login.html"

class RegisterPageView(TemplateView):
    template_name = "register.html"

class DashboardPageView(TemplateView):
    template_name = "admin/dashboard.html"

def dologin(request):
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(request, username=email, password=password)
    if user is not None:
        login(request, user)
        return redirect('public:dashboard')
    else:
        messages.error(request, "Wrong password or email combination")
        return redirect('public:login')

def doregister(request):
    email = request.POST['email']
    password = request.POST['password']
    re_password = request.POST['repeatPassword']
    first_name = request.POST['firstName']
    last_name = request.POST['lastName']
    if password != re_password:
        messages.error(request, "Passwords don't match")
        return redirect('public:register')
    else:
        try:
            User.objects.create_user(
                email=email,
                username=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            messages.error(request, "Account successfully created, please login")
            return redirect('public:login')
        except Exception as ex:
            if 'already exists' in str(ex):
                messages.error(request, "Account already exists")
            else:
                messages.error(request, "An error occurred please try again")
            return redirect('public:register')

def user_logout(request):
    logout(request)
    return redirect('public:login')