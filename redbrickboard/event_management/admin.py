from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Event, Promo, Comment, Attendance

admin.site.register(Event)
admin.site.register(Promo)
admin.site.register(Comment)
admin.site.register(Attendance)

