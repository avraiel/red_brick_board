from django.urls import path

from .views import EventListView, EventDetailView, EventCreateView, EventUpdateView

urlpatterns = [
    path('', EventListView.as_view(), name='event-list'),
    path('<int:pk>/details', EventDetailView.as_view(), name='event-details'),
    path('add/', EventCreateView.as_view(), name='event-create'),
    path('<int:pk>/update', EventUpdateView.as_view(), name='event-update'),
]

app_name = "event_management"