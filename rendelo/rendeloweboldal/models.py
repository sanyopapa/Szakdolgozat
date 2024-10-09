from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class RendeloUser(AbstractUser):
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(unique=True, max_length=11)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'mobile_number']

    def __str__(self):
        return self.email

def get_current_time():
    return timezone.now().time().isoformat()

class Doctor(models.Model):
    name = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='doctor_pictures/', null=True, blank=True)

class Treatment(models.Model):
    title = models.CharField(max_length=255)
    duration = models.DurationField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Appointment(models.Model):
    date = models.DateField(default=timezone.now)
    start_time = models.TimeField(default=get_current_time)
    end_time = models.TimeField(default=get_current_time)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    is_booked = models.BooleanField(default=False)

class Patient(models.Model):
    user = models.OneToOneField(RendeloUser, on_delete=models.CASCADE)
    previous_treatments = models.TextField()
