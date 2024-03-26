from django.urls import path

from .views import *

app_name = "accounts"

urlpatterns = [
    path('login', login_page, name="login"),
    path('register', register, name="register"),
    path('logout', user_logout, name="logout"),
    path('auth-receiver', auth_receiver, name="auth-receiver"),
    path('list', UserList.as_view(), name="list"),
    path('profile/<int:pk>', UserProfile.as_view(), name="profile")
]