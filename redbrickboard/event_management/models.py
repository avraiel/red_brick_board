from django.db import models
from django.utils import timezone
from django.urls import reverse
from datetime import timedelta
from accounts import models as accounts

class Event(models.Model):
    event_name = models.CharField(default='', max_length=150)
    event_datetime_start = models.DateTimeField(default=timezone.now, null=False)
    event_datetime_end = models.DateTimeField()
    event_organizer = models.ForeignKey(accounts.CustomUser, on_delete=models.CASCADE, related_name='events_organized')
    # finalize arguments
    event_header = models.ImageField(upload_to='headers/', height_field=None, width_field=None, max_length=100, blank=True)
    # research how exactly to do this
    event_promos = models.FileField(upload_to='promos/', blank=True, null=True)
    # decide whether to have a separate model for the comments
    comments = models.TextField()
    last_time_bumped = models.DateTimeField()

    def __str__(self):
        return '{}'.format(self.event_name)
    
    def get_absolute_url(self):
        return reverse('event_management:event_details', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if self.event_datetime_end is None:
            self.event_datetime_end = self.event_datetime_start + timedelta(hours=1)
        if self.last_time_bumped is None:
            self.last_time_bumped = self.event_datetime_start
        super(Event, self).save(*args, **kwargs)