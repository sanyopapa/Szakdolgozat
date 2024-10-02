from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Appointment
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, LoginForm
from .models import RendeloUser
from django.contrib.auth.decorators import login_required

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
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # User already created with form.save()
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
                login(request, user)
                return redirect('/')
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