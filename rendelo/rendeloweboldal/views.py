from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Appointment
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

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

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})