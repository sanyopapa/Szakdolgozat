from uuid import uuid4
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Appointment, Treatment, Doctor, Patient, RendeloUser
from django.contrib.auth import login as auth_login, authenticate, logout
from .forms import RegistrationForm, LoginForm, ProfileForm, PatientForm, TreatmentForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta

def kezdooldal(request):
    treatments = Treatment.objects.all()
    return render(request, 'kezdooldal.html', {'treatments': treatments})

def idopontfoglalas(request):
    if request.user.is_superuser or hasattr(request.user, 'doctor'):
        return render(request, 'idopontfoglalas.html', {'error_message': 'Superuser vagy doctor nem foglalhat időpontot.'})

    if request.method == 'POST':
        try:
            treatment = Treatment.objects.get(id=request.POST['treatment'])
            start_time = timezone.make_aware(datetime.strptime(request.POST['appointment_datetime'], '%Y-%m-%d %H:%M'))
            treatment_duration = treatment.duration.total_seconds() // 60

            treatment_duration = ((treatment_duration + 14) // 15) * 15
            end_time = start_time + timedelta(minutes=treatment_duration)

            current_time = start_time
            while current_time < end_time:
                if Appointment.objects.filter(practitioner_id=request.POST['selected_doctor'], start__lte=current_time, end__gt=current_time, status='booked').exists():
                    return render(request, 'idopontfoglalas.html', {'error_message': 'Az időpont foglalt.'})
                current_time += timedelta(minutes=15)

            Appointment.objects.create(
                id=str(uuid4()),
                patient=request.user.id,
                practitioner_id=request.POST['selected_doctor'],
                treatment=treatment,
                start=start_time,
                end=end_time,
                status='booked'
            )

            return redirect('profile')
        except Exception as e:
            return render(request, 'idopontfoglalas.html', {'error_message': 'Hiba történt az időpont foglalása során.'})
        
    return render(request, 'idopontfoglalas.html', {'doctors': Doctor.objects.all(), 'treatments': Treatment.objects.all()})

def admin_view(request):
    treatments = Treatment.objects.all()
    return render(request, 'admin.html', {'treatments': treatments})

@login_required
def add_treatment(request):
    if request.method == 'POST':
        form = TreatmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_view')
    else:
        form = TreatmentForm()
    return render(request, 'add_treatment.html', {'form': form})

@login_required
def edit_treatment(request, treatment_id):
    treatment = get_object_or_404(Treatment, id=treatment_id)
    if request.method == 'POST':
        form = TreatmentForm(request.POST, instance=treatment)
        if form.is_valid():
            form.save()
            return redirect('admin_view')
    else:
        form = TreatmentForm(instance=treatment)
    return render(request, 'edit_treatment.html', {'form': form, 'treatment': treatment})

@login_required
def delete_treatment(request, treatment_id):
    treatment = get_object_or_404(Treatment, id=treatment_id)
    if request.method == 'POST':
        treatment.delete()
        return redirect('admin_view')
    return render(request, 'delete_treatment.html', {'treatment': treatment})

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
        appointment.save()
    return redirect('profile')

def get_available_slots(request):
    doctor_id = request.GET.get('doctor')
    date = request.GET.get('date')
    treatment_id = request.GET.get('treatment')
    treatment = Treatment.objects.get(id=treatment_id)
    treatment_duration = treatment.duration.total_seconds() // 60

    # Felfelé kerekítés 15 perces intervallumokra
    treatment_duration = ((treatment_duration + 14) // 15) * 15

    start_time = timezone.make_aware(datetime.strptime(date, '%Y-%m-%d').replace(hour=8, minute=0, second=0))
    end_time = start_time.replace(hour=20, minute=0, second=0)

    slots = []
    current_time = start_time
    while current_time < end_time:
        slot_end_time = current_time + timedelta(minutes=treatment_duration)
        is_available = True
        check_time = current_time
        while check_time < slot_end_time:
            if Appointment.objects.filter(practitioner_id=doctor_id, start__lte=check_time, end__gt=check_time, status='booked').exists() or check_time.time() == end_time.time():
                is_available = False
                break
            check_time += timedelta(minutes=15)
        
        slots.append({
            'time': current_time.strftime('%H:%M'),
            'available': is_available
        })
        current_time += timedelta(minutes=15)

    return JsonResponse({'slots': slots})

def get_earliest_slot(request):
    doctor_id = request.GET.get('doctor')
    treatment_id = request.GET.get('treatment')
    treatment = Treatment.objects.get(id=treatment_id)
    treatment_duration = treatment.duration.total_seconds() // 60

    # Felfelé kerekítés 15 perces intervallumokra
    treatment_duration = ((treatment_duration + 14) // 15) * 15

    start_time = timezone.now() + timedelta(days=1)
    start_time = start_time.replace(hour=8, minute=0, second=0, microsecond=0)
    end_time = start_time.replace(hour=20, minute=0, second=0, microsecond=0)

    while True:
        current_time = start_time
        while current_time < end_time:
            slot_end_time = current_time + timedelta(minutes=treatment_duration)
            is_available = True
            check_time = current_time
            while check_time < slot_end_time:
                if Appointment.objects.filter(practitioner_id=doctor_id, start__lte=check_time, end__gt=check_time, status='booked').exists() or check_time.time() == end_time.time():
                    is_available = False
                    break
                check_time += timedelta(minutes=15)
            
            if is_available:
                return JsonResponse({'earliest_slot': {'date': current_time.strftime('%Y-%m-%d'), 'time': current_time.strftime('%H:%M')}})
            current_time += timedelta(minutes=15)
        
        start_time += timedelta(days=1)
        start_time = start_time.replace(hour=8, minute=0, second=0, microsecond=0)
        end_time = start_time.replace(hour=20, minute=0, second=0, microsecond=0)

    return JsonResponse({'earliest_slot': None})