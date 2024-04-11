from django.db import models
from django_resized import ResizedImageField
from django.utils import timezone
from django.urls import reverse
from accounts import models as accounts
# from datetime import timedelta

class Event(models.Model):
    event_name = models.CharField(default='', max_length=150)
    event_datetime_start = models.DateTimeField(default=timezone.now, null=False)
    event_datetime_end = models.DateTimeField(default=None, null=True)
    event_organizer = models.ForeignKey(accounts.CustomUser, on_delete=models.CASCADE, related_name='events_organized')
    event_header = ResizedImageField(size=[815, 315], crop=['middle', 'center'], quality=75, force_format='WebP', upload_to=rename_image('headers/'))
    last_time_bumped = models.DateTimeField()

    def __str__(self):
        return '{}'.format(self.event_name)
    
    def get_absolute_url(self):
        return reverse('event_management:event-details', kwargs={'pk': self.pk})

    # def save(self, *args, **kwargs):
    #     if self.event_datetime_end is None:
    #         self.event_datetime_end = self.event_datetime_start + timedelta(hours=1)
    #     if self.last_time_bumped is None:
    #         self.last_time_bumped = self.event_datetime_start
    #     super(Event, self).save(*args, **kwargs)

class Promo(models.Model):
    img = models.ImageField(upload_to='images/', height_field=None, width_field=None, max_length=100, blank=True)
    event_name = models.ForeignKey(Event, on_delete=models.CASCADE)

class Comment(models.Model):
    event_comment = models.TextField(default='', max_length=255)
    event_name = models.ForeignKey(Event, on_delete=models.CASCADE)