from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Appointment, Treatment, Doctor, Patient, RendeloUser
from django.contrib.auth import login as auth_login, authenticate, logout
from .forms import RegistrationForm, LoginForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.backends import ModelBackend

def kezdooldal(request):
    treatments = Treatment.objects.all()
    return render(request, 'kezdooldal.html', {'treatments': treatments})

def idopontfoglalas(request):
    if request.method == 'POST':
        rendelo_user_id = request.user.id
        try:
            patient = Patient.objects.get(id=rendelo_user_id)  
        except Patient.DoesNotExist:
            return HttpResponse("Nincs páciens rekord a felhasználóhoz társítva.", status=400)
        try:
            Appointment.objects.create(
                patient=patient,
                practitioner_id=request.POST['selected_doctor'],
                treatment_id=request.POST['treatment'],
                start=request.POST['appointment_datetime']
            )
            return redirect('home')
        except Exception as e:
            return JsonResponse({"error": str(e), "user_id": rendelo_user_id, "patient_id": patient.id}, status=400)
        
    return render(request, 'idopontfoglalas.html', {'doctors': Doctor.objects.all(), 'treatments': Treatment.objects.all()})

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
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=user)
    return render(request, 'profile.html', {'form': form})