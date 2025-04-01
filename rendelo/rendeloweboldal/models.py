from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from uuid import uuid4

class RendeloUser(AbstractUser):
    id = models.CharField(max_length=64, primary_key=True, default=str(uuid4()))  
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class Patient(models.Model):
    id = models.CharField(max_length=64, primary_key=True)  
    name = models.CharField(max_length=255)  
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    birthDate = models.DateField(null=True, blank=True)  
    telecom = models.CharField(max_length=255, null=True, blank=True)  

    def __str__(self):
        return self.name

class Doctor(models.Model):
    id = models.CharField(max_length=64, primary_key=True)  
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='doctor_pictures/', null=True, blank=True) 
    qualification = models.TextField(null=True, blank=True)  

    def __str__(self):
        return self.name

class Treatment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)  
    name = models.CharField(max_length=255)  
    description = models.TextField() 
    duration = models.DurationField(null=True, blank=True)  
    price = models.DecimalField(max_digits=10, decimal_places=0)  

    def __str__(self):
        return self.description

class Appointment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)  
    patient = models.CharField(max_length=64, null=True, blank=True)  
    practitioner = models.ForeignKey(Doctor, on_delete=models.CASCADE)  
    treatment = models.ForeignKey(Treatment, on_delete=models.SET_NULL, null=True, blank=True) 
    start = models.DateTimeField() 
    end = models.DateTimeField() 
    status = models.CharField(max_length=64, null=True, blank=True)  # Időpont státusza (pl. foglalt, elérhető)
    custom_description = models.TextField(null=True, blank=True)  # Időpont leírása, ezt szerkeszti a kezelőorvos

    def __str__(self):
        return f"Appointment for {self.patient} with {self.practitioner.name}"

class WorkingHours(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()

    def __str__(self):
        return f"Working hours for {self.doctor.name} on {self.date} from {self.start} to {self.end}"

class PaymentStatus(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, primary_key=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment status for appointment {self.appointment.id}: {'Paid' if self.is_paid else 'Not Paid'}"