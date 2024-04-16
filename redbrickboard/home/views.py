from django.shortcuts import render
from django.views.generic.list import ListView
from event_management.models import Event

class FeaturedEventListView(ListView):
    model = Event
    fields = '__all__'
    ordering = ['-last_time_bumped']
    template_name = 'home/index.html'