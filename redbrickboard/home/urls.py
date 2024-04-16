from django.urls import path

from .views import FeaturedEventListView

urlpatterns = [
    path('', FeaturedEventListView.as_view(), name='featured-event-list'),
]