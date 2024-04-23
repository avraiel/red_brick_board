from accounts import models as accounts
from django import forms
from django.forms import ModelForm, BaseModelFormSet, inlineformset_factory
from .models import Event, Promo

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
        exclude = ('last_time_bumped', 'event_organizer',)
        widgets = {
            'event_datetime_start':forms.TextInput(attrs={'type':'datetime-local'}),
            'event_datetime_end':forms.TextInput(attrs={'type':'datetime-local'}),
            'last_time_bumped':forms.TextInput(attrs={'type':'datetime-local'}),
        }

class PromoForm(ModelForm):
    model = Promo
    fields = "__all__"


# Source for the whole formset integration:
# https://www.letscodemore.com/blog/django-inline-formset-factory-with-examples/

PromoFormSet = inlineformset_factory(
    Event,
    Promo,
    form=PromoForm,
    extra=1,
    fields=['img'],
    can_delete=True,
    can_delete_extra=True
)