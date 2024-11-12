from uuid import uuid4
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Appointment, Treatment, Doctor, Patient, RendeloUser
from django.contrib.auth import login as auth_login, authenticate, logout
from .forms import RegistrationForm, LoginForm, ProfileForm, PatientForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.backends import ModelBackend
from django.utils import timezone

def kezdooldal(request):
    treatments = Treatment.objects.all()
    return render(request, 'kezdooldal.html', {'treatments': treatments})

def idopontfoglalas(request):
    if request.user.is_superuser or hasattr(request.user, 'doctor'):
        return HttpResponse("Superuser vagy doctor nem foglalhat időpontot.", status=403)

    if request.method == 'POST':
        try:
            Appointment.objects.create(
                id=str(uuid4()),  
                patient=request.user.id,
                practitioner_id=request.POST['selected_doctor'],
                treatment_id=request.POST['treatment'],
                start=request.POST['appointment_datetime']
            )
            return redirect('home')
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
    return render(request, 'idopontfoglalas.html', {'doctors': Doctor.objects.all(), 'treatments': Treatment.objects.all()})

def admin_view(request):
    return render(request, 'admin.html')

def register_view(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        patient_form = PatientForm(request.POST)
        if user_form.is_valid() and patient_form.is_valid():
            user = user_form.save()
            patient = patient_form.save(commit=False)
            patient.id = user.id
            patient.save()
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/')
    else:
        user_form = RegistrationForm()
        patient_form = PatientForm()
    return render(request, 'register.html', {'user_form': user_form, 'patient_form': patient_form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                return HttpResponse("Hibás bejelentkezési adatok.", status=401)
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    user = request.user
    if user.is_superuser or hasattr(user, 'doctor'):
        patient_form = None
    else:
        patient = get_object_or_404(Patient, id=user.id)
        patient_form = PatientForm(request.POST or None, instance=patient)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            if patient_form and patient_form.is_valid():
                patient_form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=user)
        if not user.is_superuser and not hasattr(user, 'doctor'):
            patient_form = PatientForm(instance=patient)
    
    appointments = Appointment.objects.filter(patient=user.id)
    return render(request, 'profile.html', {'form': form, 'patient_form': patient_form, 'appointments': appointments})

@login_required
def cancel_appointment(request, appointment_id):
    patient = get_object_or_404(Patient, id=request.user.id)
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=patient)
    if appointment.start > timezone.now():
        appointment.status = 'cancelled'
        appointment.save()
    return redirect('profile')