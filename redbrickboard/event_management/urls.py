from django.urls import path

from .views import EventListView, EventDetailView, EventCreateView, EventUpdateView, delete_image, event_rsvp

urlpatterns = [
    path('', EventListView.as_view(), name='event-list'),
    path('<int:pk>/details', EventDetailView.as_view(), name='event-details'),
    path('add/', EventCreateView.as_view(), name='event-create'),
    path('<int:pk>/update', EventUpdateView.as_view(), name='event-update'),
    path('int<pk>/delete-image', delete_image, name='delete_image'),
    path('<int:pk>/rsvp', event_rsvp, name='event-rsvp'),
]

app_name = "event_management"