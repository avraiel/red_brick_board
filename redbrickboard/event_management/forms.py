from accounts import models as accounts
from django import forms
from django.forms import ModelForm, BaseModelFormSet, inlineformset_factory
from .models import Event, Promo

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
        widgets = {
            # 'event_organizer': forms.TextInput(attrs={'disabled':'disabled'}),
            'event_datetime_start':forms.TextInput(attrs={'type':'datetime-local'}),
            'event_datetime_end':forms.TextInput(attrs={'type':'datetime-local'}),
            'last_time_bumped':forms.TextInput(attrs={'type':'datetime-local'}),
        }

        # def __init__(self, *args, **kwargs):
        #     super(EventForm, self).__init__(*args, **kwargs)
            
        #     # Set the event_organizer field to the currently logged-in user
        #     self.fields['event_organizer'].widget.attrs['readonly'] = True
        #     self.fields['event_organizer'].widget.attrs['disabled'] = True
        #     if self.instance.event_organizer:
        #         self.fields['event_organizer'].initial = self.instance.event_organizer.get_full_name()

        # def save(self, commit=True):
        #     instance = super(EventForm, self).save(commit=False)
            
        #     # If the event organizer is not set, set it to the currently logged-in user
        #     if not instance.event_organizer:
        #         instance.event_organizer = self.initial['event_organizer']
            
        #     if commit:
        #         instance.save()
        #     return instance
    
    def clean_event_organizer(self):
        # Set the event organizer to the currently logged-in user
        return self.instance.event_organizer

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