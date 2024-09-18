from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Appointment

def kezdooldal(request):
    return render(request, 'kezdooldal.html')

def idopontfoglalas(request):
    if request.method == 'POST':
        appointment_datetime = request.POST['appointment_datetime']
        treatment = request.POST['treatment']
        # Itt mentem az adatbázisba
        Appointment.objects.create(datetime=appointment_datetime, treatment=treatment)
        return redirect('home')
    return render(request, 'idopontfoglalas.html')

def admin_view(request):
    return render(request, 'admin.html')