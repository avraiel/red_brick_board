from typing import Any
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages

from .forms import (EventForm, PromoFormSet)
from .models import Event, Promo, Attendance
from django.db.models import Q 

from django.utils import timezone

# import to require users to be logged in to access certain features
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin

# This function is for custom delete button.
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

def search_events(request):
    if request.method == "POST":
        searched = request.POST['searched']
        events = Event.objects.all()
        events = Event.objects.filter(Q(event_name__icontains=searched)|Q(event_description__icontains=searched))

        return render(request, 'event_management/event-search.html', {'searched': searched, 'events':events})
    else:

        return render(request, 'event_management/event-search.html', {})


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        attendance = Attendance.objects.filter(event = event)
        context['attendance'] = attendance
        
        return context


class EventListView(ListView):
    model = Event
    fields = '__all__'
    template_name = 'event_management/event-list.html'
    
    # def get_queryset(self):
    #     return Event.objects.all().order_by('-last_time_bumped')


class FeaturedEventListView(ListView):
    model = Event
    fields = '__all__'
    queryset = Event.objects.order_by('-last_time_bumped')[:8]
    template_name = 'event_management/event-featured.html'

# Creating an event requires the user to be logged in
class EventCreateView(LoginRequiredMixin, PromoInline, CreateView):
    login_url = '/accounts/login'
    model = Event
    
    # Set the event organizer to the currently logged-in user
    def form_valid(self, form):
        form.instance.event_organizer_id = self.request.user.pk
        return super().form_valid(form)

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
        
# Updating an event requires the user to be logged in 
class EventUpdateView(LoginRequiredMixin, PromoInline, UpdateView):
    login_url = '/accounts/login'
    model = Event
    form_class = EventForm 

    # # Set the event organizer to the currently logged-in user
    # def form_valid(self, form):
    #     form.instance.event_organizer = self.request.user
    #     return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        ctx = super(EventUpdateView, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx
    
    def get_named_formsets(self):
        return {
            'images': PromoFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='images'),
        }

# Bumping an event requires the user to be logged in
@login_required(login_url="/accounts/login")
def bump_event(request, *args, **kwargs):
    # gets PK of the event
    pk = kwargs.get('pk')
    # gets Event object in Event table, based on PK
    event = get_object_or_404(Event, pk=pk)
    ## url can be accessed, check in place to prevent cheating bumps
    if event.can_be_bumped:
        event.last_time_bumped = timezone.now()
        event.save()
        messages.success(request, 'Bump Successful!')
    else:
        messages.error(request, 'Bump Not Successful :(')
    return redirect('event_management:event-details', pk = pk) 

# def event_details(request, pk):
#     event = get_object_or_404(Event, pk=pk)
#     remaining_time = event.time_until_bump()
    
#     context = {
#         'event': event,
#         'remaining_time': remaining_time
#     }
#     return render(request, 'event_details.html', context)

# To RSVP to an event, the user must be logged in
@login_required(login_url="/accounts/login")
def event_rsvp(request, *args, **kwargs):
    
    # gets PK of the event
    pk = kwargs.get('pk')
    # gets Event object in Event table, based on PK
    event = get_object_or_404(Event, pk=pk)
    # gets the currently logged in user
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

@login_required(login_url="/accounts/login")
def handle_attendance(request, *args, **kwargs):
    event_pk = kwargs.get('pk')
    event = get_object_or_404(Event, pk=event_pk)
    user = request.user

    if event.event_organizer.pk != user.pk:
        # this conditional ensures that non-organizers cannot handle attendance
        messages.error(request, 'You may not handle attendance for this event')
    else:
        records = Attendance.objects.filter(Q(event_id=event_pk))

        attended = []
        for attendance_key, value in request.POST.items():
            if attendance_key != "csrfmiddlewaretoken":
                attended.append(int(attendance_key))
        # post data = lahat ng naka-check 

        for record in records:
            record.has_attended = 0
            if int(record.pk) in attended:
                record.has_attended = 1
            record.save()
        
            
        messages.success(request, 'Attendance saved!')
    return redirect('event_management:event-details', pk = event_pk)