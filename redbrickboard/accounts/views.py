import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests

from .forms import CustomUserCreationForm, CustomUserAuthenticationForm
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django import forms

from . import models
from django.utils import timezone


def register(request):
    # return HttpResponse("I am in Register")
    form = CustomUserCreationForm()
    print(request.POST)
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
        
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
                return redirect('home')

    context = {
        'loginform' : form
    }
    
    return render(request, 'accounts/login.html', context = context)

def user_logout(request):
    auth.logout(request)
    return redirect('home')

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
    if "@ateneo.edu" not in email and "@student.ateneo.edu" not in email and "@alumni.ateneo.edu" not in email:   
        return HttpResponse("Your login must be an ateneo email address. Try again <a href='./login'>here</a>", status=403)
    if logInUser is not None:
        auth.login(request, logInUser)
    else:
        first_name = user_data['given_name']
        last_name = user_data['family_name']
        role = "STUDENT"
        user = models.CustomUser.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name, role=role)
        auth.login(request, logInUser)
    
    print("Login Successful")
    # TODO: change up this
    return redirect('home')


class UserProfile(DetailView):
    model = models.CustomUser
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Retrieve the user object
        user = self.get_object()

        # Retrieve the organized events for the user
        events_organized = user.events_organized.all().order_by('event_datetime_start')

        events_attendee = user.events_attendee.all()
        


        # Add organized_events to the context
        context['events_organized'] = events_organized
        context['events_attendee'] = events_attendee
        context['datetime_now'] = timezone.now()

        return context

class UserList(ListView):
    model = models.CustomUser
    template_name = 'accounts/list.html'

class ProfileUpdateView(UpdateView):
    model = models.CustomUser
    fields = ['first_name', 'last_name', 'bio', 'picture']
    template_name = 'accounts/profile_edit.html'