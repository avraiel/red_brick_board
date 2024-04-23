from django.urls import path

from .views import EventListView, EventDetailView, EventCreateView, EventUpdateView, FeaturedEventListView, delete_image, search_events, bump_event, event_rsvp, handle_attendance



urlpatterns = [
    path('', EventListView.as_view(), name='event-list'),
    path('<int:pk>/', EventDetailView.as_view(), name='event-details'),
    path('create/', EventCreateView.as_view(), name='event-create'),
    path('<int:pk>/update/', EventUpdateView.as_view(), name='event-update'),
    path('featured/', FeaturedEventListView.as_view(), name='event-featured'),
    path('int<pk>/delete-image', delete_image, name='delete_image'),
    path('search', search_events, name='event-search'),
    path('<int:pk>/bump-event', bump_event, name="bump-event"),
    path('<int:pk>/rsvp', event_rsvp, name='event-rsvp'),
    path('<int:pk>/handle-attendance', handle_attendance, name='event-attendance'),
]

app_name = "event_management"