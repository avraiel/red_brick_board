from typing import Any
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages

from .forms import (EventForm, PromoFormSet)
from .models import Event, Promo, Attendance

def delete_image(request, pk):
    try:
        image = Promo.objects.get(id=pk)
    except Promo.DoesNotExist:
        messages.success(
            request, 'Object Does not exist'
        )
        return redirect('event_management:event-update', pk=image.event.id)

    image.delete()
    messages.success(
        request, 'Image deleted successfully'
    )
    return redirect('event_management:event-update', pk=image.event.id)

class PromoInline():
    form_class = EventForm
    template_name = 'event_management/event-form.html'

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))
        self.object = form.save()

        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('event_management:event-list')

    def formset_images_valid(self, formset):
        images = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for image in images:
            image.event = self.object
            image.save()

class EventDetailView(DetailView):
    model = Event
    fields = '__all__'
    template_name = 'event_management/event-details.html'

class EventListView(ListView):
    model = Event
    fields = '__all__'
    template_name = 'event_management/event-list.html'

# class EventCreateView(CreateView):
#     model = Event
#     form_class = EventForm
#     success_url = '/events/'
#     template_name = 'event_management/event-form.html'

# class EventUpdateView(UpdateView):
#     model = Event
#     fields = '__all__'
#     # success_url = 
#     template_name = 'event_management/event-form.html'

class EventCreateView(PromoInline, CreateView):
    model = Event
    def get_context_data(self, **kwargs):
        ctx = super(EventCreateView, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx
    
    def get_named_formsets(self):
        if self.request.method == "GET":
            return{
                'images': PromoFormSet(prefix='images')
            }
        else:
            return{
                'images': PromoFormSet(self.request.POST or None, self.request.FILES or None, prefix='images')
            }
        
class EventUpdateView(PromoInline, UpdateView):
    model = Event
    def get_context_data(self, **kwargs):
        ctx = super(EventUpdateView, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx
    
    def get_named_formsets(self):
        return {
            'images': PromoFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='images'),
        }
    
def event_rsvp(request, *args, **kwargs):
    
    pk = kwargs.get('pk')
    event = get_object_or_404(Event, pk=pk)
    user = request.user
    
    if event.event_organizer == user:
        # this conditional ensures that organizers cannot rsvp for their events
        messages.error(request, 'You may not register for this event')
    else:
        # this conditional ensures that rsvp only happens once
        check_rsvp = Attendance.objects.filter(event = event).filter(attendee = user)
        if check_rsvp:
            messages.error(request, 'You have already registered for this event')
        else:
            Attendance.objects.create(event = event, attendee = user)
            messages.success(request, 'RSVP Successful!')
    return redirect('event_management:event-details', pk = pk)