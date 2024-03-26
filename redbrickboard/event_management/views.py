from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView

from .models import Event

def event_view(request):
    events = Event.objects.all()
    context = {'events' : events}
    return render(request, 'event_management/events.html', context)

class EventDetailView(DetailView):
    model = Event
    template_name = 'event_management/event-details.html'

class EventListView(ListView):
    model = Event
    template_name = 'event_management/event-list.html'

class EventCreateView(CreateView):
    model = Event
    fields = '__all__'
    template_name = 'event_management/event-create.html'

class EventUpdateView(UpdateView):
    model = Event
    fields = '__all__'
    template_name = 'event/event-update.html'