from django.shortcuts import render, get_object_or_404
import json	
from django.http import Http404
import json
import requests
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, auth
from .models import Profile
from django.http import HttpResponse
from django.http import JsonResponse

# Create your views here.


def register(request):
    r_user = request.user
    if r_user.is_authenticated:
        return redirect("/dashboard")
    else:
        if request.method == "POST":
            name = request.POST['name']
            email = request.POST['email']
            company = request.POST['company']
            username = request.POST['email']
            password = request.POST['password']
            
            if User.objects.filter(email=email).exists():
                return JsonResponse("<p class='error-alert' style='text-align:center'>E-mail already in use<p>", safe=False)
            else:
                user = User.objects.create_user(username=username, password=password, email=email, first_name=name)
                user.save()
                userp = User.objects.get(email=email)
                userp.profile.company = company
                userp.save()

                return JsonResponse("<p class='success-alert' style='text-align:center'>Registration successful<p><script>window.location.href = '../login';</script>", safe=False)
        return render(request, "accounts/signup.html")

def login(request):
    r_user = request.user
    if r_user.is_authenticated:
        return redirect("/dashboard")
    else:
        if request.method == "POST":
            password = request.POST['password']
            email = request.POST['email']

            if User.objects.filter(email=email).exists():
                c_user = User.objects.get(email=email)
                username = c_user.username
                user = auth.authenticate(username=username,password=password)
                if user is not None:
                    auth.login(request, user)
                    return JsonResponse("<p class='success-alert' style='text-align:center'>Login successful<p><script>window.location.href = '../dashboard';</script>", safe=False)
                    return redirect("/dashboard")
                else:
                    return JsonResponse("<p class='error-alert' style='text-align:center'>Wrong email address or password<p>", safe=False)

            else:
                return JsonResponse("<p class='error-alert' style='text-align:center'>Email address does not exist<p>", safe=False)

        return render(request, "accounts/login.html")

def dashboard(request):
    r_user = request.user
    if r_user.is_authenticated:
        return render(request, "dashboard.html")
    return redirect("/login")

def logout(request):
    auth.logout(request)
    return redirect("/login")