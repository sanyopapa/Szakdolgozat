from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    is_admin = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',  
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

def get_current_time():
    return timezone.now().time().isoformat()

class Doctor(models.Model):
    name = models.CharField(max_length=255)

class Treatment(models.Model):
    title = models.CharField(max_length=255)
    duration = models.DurationField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Appointment(models.Model):
    date = models.DateField(default='2024-01-01')
    start_time = models.TimeField(default=get_current_time)
    end_time = models.TimeField(default=get_current_time)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, default=1)
    is_booked = models.BooleanField(default=False)

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    previous_treatments = models.TextField()