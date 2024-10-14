from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Appointment, Treatment, Doctor, Patient
from django.contrib.auth import login as auth_login, authenticate, logout
from .forms import RegistrationForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.backends import ModelBackend

def kezdooldal(request):
    treatments = Treatment.objects.all()
    return render(request, 'kezdooldal.html', {'treatments': treatments})

def idopontfoglalas(request):
    if request.method == 'POST':
        appointment_datetime = request.POST['appointment_datetime']
        treatment_id = request.POST['treatment']
        selected_doctor_id = request.POST['selected_doctor']
        doctor = Doctor.objects.get(id=selected_doctor_id)
        treatment = Treatment.objects.get(id=treatment_id)
        Appointment.objects.create(
            start=appointment_datetime,
            treatment=treatment,
            practitioner=doctor,
            patient=request.user.patient  # Assuming the user has a related patient object
        )
        return redirect('home')
    doctors = Doctor.objects.all()
    treatments = Treatment.objects.all()
    return render(request, 'idopontfoglalas.html', {'doctors': doctors, 'treatments': treatments})

def admin_view(request):
    return render(request, 'admin.html')

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('home')
            else:
                form.add_error(None, "Helytelen bejelentkezési adatok.")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})