from uuid import uuid4
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Appointment, Treatment, Doctor, Patient, RendeloUser
from django.contrib.auth import login as auth_login, authenticate, logout
from .forms import RegistrationForm, LoginForm, ProfileForm, PatientForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

def kezdooldal(request):
    treatments = Treatment.objects.all()
    return render(request, 'kezdooldal.html', {'treatments': treatments})

def idopontfoglalas(request):
    if request.user.is_superuser or hasattr(request.user, 'doctor'):
        return HttpResponse("Superuser vagy doctor nem foglalhat időpontot.", status=403)

    if request.method == 'POST':
        try:
            treatment = Treatment.objects.get(id=request.POST['treatment'])
            start_time = timezone.datetime.strptime(request.POST['appointment_datetime'], '%Y-%m-%d %H:%M')
            end_time = start_time + treatment.duration

            # Ellenőrizzük, hogy az összes szükséges időpont szabad-e
            current_time = start_time
            while current_time < end_time:
                if Appointment.objects.filter(practitioner_id=request.POST['selected_doctor'], start=current_time, status='booked').exists():
                    return JsonResponse({"error": "Az időpont már foglalt."}, status=400)
                current_time += timedelta(minutes=15)

            # Foglaljuk le az összes szükséges időpontot
            current_time = start_time
            while current_time < end_time:
                Appointment.objects.create(
                    id=str(uuid4()),
                    patient=request.user.id,
                    practitioner_id=request.POST['selected_doctor'],
                    treatment=treatment,
                    start=current_time,
                    end=current_time + timedelta(minutes=15),
                    status='booked'
                )
                current_time += timedelta(minutes=15)

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
    
    appointments = Appointment.objects.filter(patient=user.id, status='booked')
    now = timezone.now()
    return render(request, 'profile.html', {'form': form, 'patient_form': patient_form, 'appointments': appointments, 'now': now})

@login_required
def cancel_appointment(request, appointment_id):
    appointments = Appointment.objects.filter(id=appointment_id, patient=request.user.id, status='booked')
    for appointment in appointments:
        appointment.status = 'available'
        appointment.patient = None
        appointment.save()
    return redirect('profile')

def get_available_slots(request):
    doctor_id = request.GET.get('doctor')
    date = request.GET.get('date')
    start_time = timezone.datetime.strptime(date, '%Y-%m-%d').replace(hour=8, minute=0, second=0)
    end_time = start_time.replace(hour=20, minute=0, second=0)

    slots = []
    current_time = start_time
    while current_time < end_time:
        slot = {
            'time': current_time.strftime('%H:%M'),
            'available': not Appointment.objects.filter(practitioner_id=doctor_id, start=current_time, status='booked').exists()
        }
        slots.append(slot)
        current_time += timedelta(minutes=15)

    return JsonResponse({'slots': slots})