from django.urls import path

from .views import EventListView, EventDetailView, EventCreateView, EventUpdateView, delete_image, bump_event

urlpatterns = [
    path('', EventListView.as_view(), name='event-list'),
    path('<int:pk>/details', EventDetailView.as_view(), name='event-details'),
    path('add/', EventCreateView.as_view(), name='event-create'),
    path('<int:pk>/update', EventUpdateView.as_view(), name='event-update'),
    path('int<pk>/delete-image', delete_image, name='delete_image'),
    path('<int:pk>/bump-event', bump_event, name="bump-event")
]

app_name = "event_management"