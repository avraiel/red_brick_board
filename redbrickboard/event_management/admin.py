from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Event, Attendance

admin.site.register(Event)
admin.site.register(Attendance)