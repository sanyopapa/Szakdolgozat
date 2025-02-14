from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import RendeloUser, Doctor, Treatment, Appointment, Patient, WorkingHours

class RendeloUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email') 

admin.site.register(RendeloUser, RendeloUserAdmin)
admin.site.register(Doctor)
admin.site.register(Treatment)
admin.site.register(Appointment)
admin.site.register(Patient)
admin.site.register(WorkingHours)