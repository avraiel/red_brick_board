import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests

from .forms import CustomUserCreationForm, CustomUserAuthenticationForm


from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout


from . import models


def register(request):
    # return HttpResponse("I am in Register")
    form = CustomUserCreationForm()
    print(request.POST)
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
        
    context = {
        'registerform': form,
    }
    return render(request, 'accounts/register.html', context = context)

def login_page(request):
    form = CustomUserAuthenticationForm()
    print(request.POST)
    if request.method == "POST":
        form = CustomUserAuthenticationForm(request, data = request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, email = email, password = password)
            if user is not None:
                auth.login(request, user)
                return redirect("index")

    context = {
        'loginform' : form
    }
    
    return render(request, 'accounts/login.html', context = context)

def user_logout(request):
    auth.logout(request)
    return redirect("index")

@csrf_exempt
def auth_receiver(request):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
    token = request.POST['credential']

    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), os.environ['GOOGLE_OAUTH_CLIENT_ID']
        )
    except ValueError:
        return HttpResponse(status=403)


    # In a real app, I'd also save any new user here to the database. See below for a real example I wrote for Photon Designer.
    # You could also authenticate the user here using the details from Google (https://docs.djangoproject.com/en/4.2/topics/auth/default/#how-to-log-a-user-in)
    
    email = user_data['email']
    password = user_data['sub']+'google'+user_data['name']

    logInUser = authenticate(request, email = email, password = password)

    if logInUser is not None:
        pass
    else:
        first_name = user_data['given_name']
        last_name = user_data['family_name']
        role = "STUDENT"
        user = models.CustomUser.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name, role=role)

    auth.login(request, logInUser)
    print("Login Successful")
    return redirect("index")
    