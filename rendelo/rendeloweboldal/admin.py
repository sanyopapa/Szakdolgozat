from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Doctor, Treatment, Appointment, Patient

admin.site.register(User, UserAdmin)
admin.site.register(Doctor)
admin.site.register(Treatment)
admin.site.register(Appointment)
admin.site.register(Patient)