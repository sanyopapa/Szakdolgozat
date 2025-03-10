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
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)  # FHIR resource identifier
    name = models.CharField(max_length=255)  # FHIR 'name' field
    description = models.TextField()  # FHIR 'description' field
    duration = models.DurationField(null=True, blank=True)  # Kezelés hossza (opcionális)
    price = models.DecimalField(max_digits=10, decimal_places=0)  # Ár

    def __str__(self):
        return self.description

class Appointment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)  # FHIR resource identifier
    patient = models.CharField(max_length=64, null=True, blank=True)  # Az időpontot foglaló páciens azonosítója
    practitioner = models.ForeignKey(Doctor, on_delete=models.CASCADE)  # Link to Practitioner resource
    treatment = models.ForeignKey(Treatment, on_delete=models.SET_NULL, null=True, blank=True)  # Link to Treatment
    start = models.DateTimeField()  # Kezdési időpont
    end = models.DateTimeField()  # Befejezési időpont
    status = models.CharField(max_length=64, null=True, blank=True)  # Időpont státusza (pl. foglalt, elérhető)
    custom_description = models.TextField(null=True, blank=True)  # Egyéb információk

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