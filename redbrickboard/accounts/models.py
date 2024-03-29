from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class CustomUserManager(UserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email for user must be set.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

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

    objects = CustomUserManager()

    def __str__(self):
        return self.first_name