from django.urls import path

from .views import EventHomeListView

urlpatterns = [
    path('', EventHomeListView.as_view(), name='home'),
]