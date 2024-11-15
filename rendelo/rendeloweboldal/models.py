from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from uuid import uuid4

class RendeloUser(AbstractUser):
    id = models.CharField(max_length=64, primary_key=True, default=str(uuid4()))  # FHIR resource identifier
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class Patient(models.Model):
    id = models.CharField(max_length=64, primary_key=True)  # same as RendeloUser.id
    name = models.CharField(max_length=255)  # FHIR 'name' field
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    birthDate = models.DateField(null=True, blank=True)  # FHIR 'birthDate' field
    telecom = models.CharField(max_length=255, null=True, blank=True)  # FHIR 'telecom' field for contact details

    def __str__(self):
        return self.name

class Doctor(models.Model):
    id = models.CharField(max_length=64, primary_key=True)  # FHIR resource identifier
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='doctor_pictures/', null=True, blank=True)  # FHIR 'photo' field
    qualification = models.TextField(null=True, blank=True)  # FHIR 'qualification' field

    def __str__(self):
        return self.name

class Treatment(models.Model):
    id = models.CharField(max_length=64, primary_key=True)  # FHIR resource identifier
    code = models.CharField(max_length=255)  # FHIR 'code' field for treatment code
    description = models.TextField()  # FHIR 'description' field
    duration = models.DurationField(null=True, blank=True)  # Kezelés hossza (opcionális)
    price = models.DecimalField(max_digits=10, decimal_places=0)  # Ár

    def __str__(self):
        return self.description

class Appointment(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=uuid4)  # FHIR resource identifier
    patient = models.CharField(max_length=64)  # Az időpontot foglaló páciens azonosítója
    practitioner = models.ForeignKey(Doctor, on_delete=models.CASCADE)  # Link to Practitioner resource
    treatment = models.ForeignKey(Treatment, on_delete=models.SET_NULL, null=True, blank=True)  # Link to Treatment
    start = models.DateTimeField(default=timezone.now)  # FHIR 'start' field
    end = models.DateTimeField(default=timezone.now)  # FHIR 'end' field
    status = models.CharField(max_length=20, default='available', choices=[('available', 'Available'), ('booked', 'Booked'), ('cancelled', 'Cancelled')])

    def __str__(self):
        return f"Appointment for {self.patient} with {self.practitioner.name}"
