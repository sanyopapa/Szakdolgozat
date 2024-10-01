from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import RendeloUser, Doctor, Treatment, Appointment, Patient

admin.site.register(RendeloUser)
admin.site.register(Doctor)
admin.site.register(Treatment)
admin.site.register(Appointment)
admin.site.register(Patient)