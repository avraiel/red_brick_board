from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ("STUDENT", "Student"),
        ("ORG", "Organization"),
        ("ALUMNI", "Alumni"),
        ("FACULTY", "Faculty"),
    ]
    
    username = None
    email = models.EmailField(unique=True, db_index=True)
    first_name = models.CharField(blank=False, max_length=150)
    last_name = models.CharField(blank=False, max_length=150)
    role = models.CharField(max_length=7, blank=False, choices=ROLE_CHOICES)
    bio = models.TextField(blank=True, max_length=150)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.first_name