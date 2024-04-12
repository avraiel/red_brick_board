from accounts import models as accounts
from django import forms
from django.forms import ModelForm
from .models import Event

# class EventForm(forms.ModelForm):
#     class Meta:
#         model = Event
#         fields = ["event_name", "event_datetime_start", "event_datetime_end", "event_organizer", "event_header", "last_time_bumped"]

class EventForm(ModelForm):
    # event_name = forms.CharField(label='Event Name', max_length=150)
    # event_datetime_start = forms.DateTimeField(label='Event Start Date and Time')
    # event_datetime_end = forms.DateTimeField(label='Event End Date and Time')
    # event_organizer = forms.ModelChoiceField(label='Event Organizer', queryset=accounts.CustomUser.objects.all())
    # event_header = forms.ImageField(label='Event Header Photo')
    # last_time_bumped = forms.DateTimeField(label='Last Time Bump')
    class Meta:
        model = Event
        fields = "__all__"
        # fields = ["event_name", "event_datetime_start", "event_datetime_end",
        #           "event_organizer", "event_header", "last_time_bumped"]
        # fields = ["event_datetime_start"]
        widgets = {
            'event_datetime_start':forms.TextInput(attrs={'type':'datetime-local'}),
            'event_datetime_end':forms.TextInput(attrs={'type':'datetime-local'}),
            'last_time_bumped':forms.TextInput(attrs={'type':'datetime-local'}),
        }