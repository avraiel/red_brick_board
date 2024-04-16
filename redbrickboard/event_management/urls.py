from django.urls import path

from .views import EventListView, EventDetailView, EventCreateView, EventUpdateView, FeaturedEventListView, delete_image, search_events


urlpatterns = [
    path('', EventListView.as_view(), name='event-list'),
    path('<int:pk>/', EventDetailView.as_view(), name='event-details'),
    path('create/', EventCreateView.as_view(), name='event-create'),
    path('<int:pk>/update/', EventUpdateView.as_view(), name='event-update'),
    path('featured/', FeaturedEventListView.as_view(), name='featured_events'),
    path('int<pk>/delete-image', delete_image, name='delete_image'),
    path('search', search_events, name='event-search'),
]

app_name = "event_management"