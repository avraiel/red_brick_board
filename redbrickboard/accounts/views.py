from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CustomUserCreationForm, CustomUserAuthenticationForm


from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout

def register(request):
    # return HttpResponse("I am in Register")
    form = CustomUserCreationForm()

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