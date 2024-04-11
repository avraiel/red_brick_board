from typing import Any
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView

from .forms import EventForm
from .models import Event    

class EventDetailView(DetailView):
    model = Event
    template_name = 'event_management/event-details.html'

class EventListView(ListView):
    model = Event
    fields = '__all__'
    template_name = 'event_management/event-list.html'

class EventCreateView(CreateView):
    model = Event
    fields = '__all__'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = EventForm()
        return context

    def post(self, request, *args, **kwargs):
        form = EventForm(request.POST)

        if form.is_valid():
            return self.get(request, *args, **kwargs)
        else:
            return render(request, self.template_name, {'form': form})

    template_name = 'event_management/event-form.html'

class EventUpdateView(UpdateView):
    model = Event
    fields = '__all__'
    template_name = 'event_management/event-form.html'