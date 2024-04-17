from django.shortcuts import render
from django.views.generic.list import ListView
from event_management.models import Event

class FeaturedEventListView(ListView):
    model = Event
    fields = '__all__'
    queryset = Event.objects.order_by('-last_time_bumped')[:3]
    template_name = 'home/index.html'