import os
from django.db import models
from django_resized import ResizedImageField
from django.utils import timezone
from django.urls import reverse
from accounts import models as accounts
from uuid import uuid4

class Event(models.Model):
    event_name = models.CharField(default='', max_length=150)
    event_description = models.TextField(default='', max_length=255)
    event_datetime_start = models.DateTimeField(default=timezone.now, null=False)
    event_datetime_end = models.DateTimeField(default=None, null=True)
    event_organizer = models.ForeignKey(accounts.CustomUser, on_delete=models.CASCADE, related_name='events_organized')
    event_header = ResizedImageField(quality=75, force_format='WebP', upload_to='headers/')
    last_time_bumped = models.DateTimeField()

    def __str__(self):
        return '{}'.format(self.event_name)
    
    def get_absolute_url(self):
        return reverse('event_management:event-details', kwargs={'pk': self.pk})
    
    def get_update_url(self):
        return reverse('event_management:event-update', kwargs={'pk': self.pk})

    ## An event can be bumped if it has been 10 minutes since the last bump
    @property
    def can_be_bumped(self):
        time_difference = timezone.now() - self.last_time_bumped
        minute_difference = time_difference.total_seconds() // 60
        if minute_difference >= 10:
            return True
        return False
    # def save(self, *args, **kwargs):
    #     if self.event_datetime_end is None:
    #         self.event_datetime_end = self.event_datetime_start + timedelta(hours=1)
    #     if self.last_time_bumped is None:
    #         self.last_time_bumped = self.event_datetime_start
    #     super(Event, self).save(*args, **kwargs)

class Promo(models.Model):
    event = models.ForeignKey(
        Event,
        related_name="promos",
        on_delete=models.CASCADE,
        null=True)
    img = ResizedImageField(quality=75, force_format='WebP', upload_to='promos/')

    def __str__(self):
        return self.event.event_name
    
    def get_absolute_url(self):
        return reverse('event_management:event-details', kwargs={'pk': self.pk})

# class Comment(models.Model):
#     event_name = models.ForeignKey(Event, on_delete=models.CASCADE)
#     event_commenter = models.ForeignKey(accounts.CustomUser, default='', on_delete=models.CASCADE, related_name='event_commenter')
#     event_comment = models.TextField(default='', max_length=255)
#     comment_created = models.DateTimeField(default=timezone.now, null=False)
#     comment_updated = models.DateTimeField(default=timezone.now, null=False)
    
#     class Meta:
#         ordering = ['-comment_updated']
    
#     def __str__(self):
#         return 'Comment by {}: {}'.format(self.event_commenter, self.event_comment)
    

class Attendance(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_attended')
    attendee = models.ForeignKey(accounts.CustomUser, on_delete=models.CASCADE)
    has_attended = models.BooleanField(default=False)
