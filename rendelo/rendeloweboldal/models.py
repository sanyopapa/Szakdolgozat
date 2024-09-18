from django.db import models

class Appointment(models.Model):
    datetime = models.DateTimeField()
    treatment = models.CharField(max_length=100)
