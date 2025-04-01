import json
from uuid import uuid4
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Appointment, Treatment, Doctor, Patient, RendeloUser, WorkingHours, PaymentStatus
from django.contrib.auth import login as auth_login, authenticate, logout
from .forms import AppointmentForm, RegistrationForm, LoginForm, ProfileForm, PatientForm, TreatmentForm, DoctorForm, CustomUserCreationForm, WorkingHoursForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm
import logging
from django.views.decorators.csrf import csrf_exempt
from django.forms import modelformset_factory
from django.contrib import messages
import os
from django.conf import settings
from django.core.mail import send_mail
from django.utils.timezone import make_aware

logger = logging.getLogger(__name__)

def kezdooldal(request):
    treatments = Treatment.objects.all()
    return render(request, 'kezdooldal.html', {'treatments': treatments})

def idopontfoglalas(request):
    if request.user.is_superuser or hasattr(request.user, 'doctor'):
        return render(request, 'idopontfoglalas.html', {'error_message': 'Superuser vagy doctor nem foglalhat időpontot.'})

    if request.method == 'POST':
        try:
            treatment = Treatment.objects.get(id=request.POST['treatment'])
            start_time = make_aware(datetime.strptime(request.POST['appointment_datetime'], '%Y-%m-%d %H:%M'))
            treatment_duration = treatment.duration.total_seconds() // 60

            treatment_duration = ((treatment_duration + 14) // 15) * 15
            end_time = start_time + timedelta(minutes=treatment_duration)

            current_time = start_time
            while current_time < end_time:
                if Appointment.objects.filter(practitioner_id=request.POST['selected_doctor'], start__lte=current_time, end__gt=current_time, status='booked').exists():
                    return render(request, 'idopontfoglalas.html', {'error_message': 'Az időpont foglalt.'})
                current_time += timedelta(minutes=15)

            working_hours = WorkingHours.objects.filter(doctor_id=request.POST['selected_doctor'], date=start_time.date())
            if not working_hours.exists():
                return render(request, 'idopontfoglalas.html', {'error_message': 'Az orvosnak nincs munkaideje ezen a napon.'})

            doctor = Doctor.objects.get(id=request.POST['selected_doctor'])
            doctoruser = RendeloUser.objects.get(id=request.POST['selected_doctor'])

            appointment = Appointment.objects.create(
                id=str(uuid4()),
                patient=request.user.id,
                practitioner_id=request.POST['selected_doctor'],
                treatment=treatment,
                start=start_time,
                end=end_time,
                status='booked'
            )

            payment_status = PaymentStatus.objects.create(
                appointment=appointment,
                is_paid=False
            )

            patient = Patient.objects.get(id=request.user.id)

            send_mail(
                'Időpontfoglalás visszaigazolása',
                f'Kedves {request.user.username},\n\nSikeresen lefoglalta az időpontot a következő kezelésre: {treatment.name}.\n\nIdőpont: {start_time.strftime("%Y-%m-%d %H:%M")}\nOrvos: {doctor.name}\n\nÜdvözlettel,\nMosolyfogaszat.hu',
                'your_email@example.com',
                [request.user.email],
                fail_silently=False,
            )

            send_mail(
                'Új időpontfoglalás',
                f'Kedves {doctor.name},\n\nÚj időpontfoglalás érkezett Önhöz.\n\nPáciens: {patient.name}\nIdőpont: {start_time.strftime("%Y-%m-%d %H:%M")}\nKezelés: {treatment.name}\nTelefonszám: {patient.telecom}\nEmail cím: {request.user.email}\n\nÜdvözlettel,\nMosolyfogaszat.hu',
                'your_email@example.com',
                [doctoruser.email],
                fail_silently=False,
            )

            if request.POST['payment_method'] == 'pay_now':
                return redirect('payment_page', appointment_id=appointment.id)
            else:
                payment_status.is_paid = False
                payment_status.save()
                return redirect('profile')
        except Exception as e:
            return render(request, 'idopontfoglalas.html', {'error_message': 'Hiba történt az időpont foglalása során.'})
        
    return render(request, 'idopontfoglalas.html', {'doctors': Doctor.objects.all(), 'treatments': Treatment.objects.all()})

@login_required
def payment_page(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        payment_status = get_object_or_404(PaymentStatus, appointment=appointment)
        payment_status.is_paid = True
        payment_status.save()
        return redirect('profile')
    return render(request, 'payment_page.html', {'appointment': appointment})

@login_required
def admin_view(request):
    if not (request.user.is_superuser):
        return redirect('home')
    
    search_query = request.GET.get('search', '')
    if search_query:
        users = RendeloUser.objects.filter(username__icontains=search_query)
    else:
        users = RendeloUser.objects.all()
    
    treatments = Treatment.objects.all()
    doctors = Doctor.objects.all()
    return render(request, 'admin.html', {'treatments': treatments, 'doctors': doctors, 'users': users})

@login_required
def add_treatment(request):
    if not (request.user.is_superuser):
        return redirect('home')
    
    if request.method == 'POST':
        form = TreatmentForm(request.POST)
        if form.is_valid():
            treatment = form.save(commit=False)
            treatment.duration = form.cleaned_data['duration']
            treatment.save()
            return redirect('admin_view')
    else:
        form = TreatmentForm()
    return render(request, 'add_treatment.html', {'form': form})

@login_required
def edit_treatment(request, treatment_id):
    if not (request.user.is_superuser):
        return redirect('home')
    
    treatment = get_object_or_404(Treatment, id=treatment_id)
    if request.method == 'POST':
        form = TreatmentForm(request.POST, instance=treatment)
        if form.is_valid():
            treatment = form.save(commit=False)
            treatment.duration = form.cleaned_data['duration']
            treatment.save()
            return redirect('admin_view')
    else:
        form = TreatmentForm(instance=treatment)
    return render(request, 'edit_treatment.html', {'form': form, 'treatment': treatment})

@login_required
def delete_treatment(request, treatment_id):
    if not (request.user.is_superuser):
        return redirect('home')
    
    treatment = get_object_or_404(Treatment, id=treatment_id)
    if request.method == 'POST':
        treatment.delete()
        return redirect('admin_view')
    return render(request, 'delete_treatment.html', {'treatment': treatment})

@login_required
def add_doctor(request):
    if not (request.user.is_superuser):
        return redirect('home')
    
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        doctor_form = DoctorForm(request.POST, request.FILES)
        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save(commit=False)
            user.is_staff = True
            user.save()
            doctor = doctor_form.save(commit=False)
            doctor.id = user.id
            doctor.save()

            send_mail(
                'Orvosi fiók létrehozása',
                f'Kedves {user.username},\n\nAz orvosi fiókja sikeresen létrehozásra került.\n\nFelhasználónév: {user.username}\nEmail cím: {user.email}\nJelszó: {request.POST["password1"]}\n\nKérjük, hogy a biztonság érdekében változtassa meg a jelszavát a bejelentkezést követően.\n\nÜdvözlettel,\nMosolyfogaszat.hu',
                'your_email@example.com',
                [user.email],
                fail_silently=False,
            )

            return redirect('admin_view')
        else:
            logger.error("User form or doctor form is not valid: %s, %s", user_form.errors, doctor_form.errors)
    else:
        user_form = CustomUserCreationForm()
        doctor_form = DoctorForm()
    return render(request, 'add_doctor.html', {'user_form': user_form, 'doctor_form': doctor_form})

@login_required
def edit_doctor(request, doctor_id):
    if not (request.user.is_superuser):
        return redirect('home')
    
    doctor = get_object_or_404(Doctor, id=doctor_id)
    user = get_object_or_404(RendeloUser, id=doctor_id)
    old_photo_path = doctor.photo.path if doctor.photo else None

    if request.method == 'POST':
        user_form = ProfileForm(request.POST, instance=user)
        doctor_form = DoctorForm(request.POST, request.FILES, instance=doctor)
        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save(commit=False)
            if user_form.cleaned_data['password1']:
                user.set_password(user_form.cleaned_data['password1'])
            user.save()
            doctor = doctor_form.save(commit=False)
            if 'photo' in request.FILES and old_photo_path:
                if os.path.exists(old_photo_path):
                    os.remove(old_photo_path)
            doctor.save()
            return redirect('admin_view')
    else:
        user_form = ProfileForm(instance=user)
        doctor_form = DoctorForm(instance=doctor)
    return render(request, 'edit_doctor.html', {'user_form': user_form, 'doctor_form': doctor_form, 'doctor': doctor})

@login_required
def delete_doctor(request, doctor_id):
    if not (request.user.is_superuser):
        return redirect('home')
    
    doctor = get_object_or_404(Doctor, id=doctor_id)
    user = get_object_or_404(RendeloUser, id=doctor_id)
    photo_path = doctor.photo.path if doctor.photo else None

    if request.method == 'POST':
        if photo_path and os.path.exists(photo_path):
            os.remove(photo_path)
        user.delete()
        doctor.delete()
        return redirect('admin_view')
    return render(request, 'delete_doctor.html', {'doctor': doctor})

@login_required
def edit_user(request, user_id):
    if not (request.user.is_superuser):
        return redirect('home')

    user = get_object_or_404(RendeloUser, id=user_id)
    patient = None
    if not user.is_superuser:
        patient = get_object_or_404(Patient, id=user_id)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        patient_form = PatientForm(request.POST, instance=patient) if patient else None
        if form.is_valid() and (patient_form is None or patient_form.is_valid()):
            user = form.save(commit=False)
            if form.cleaned_data['password1']:
                user.set_password(form.cleaned_data['password1'])
            user.save()
            if patient_form:
                patient_form.save()
            return redirect('admin_view')
    else:
        form = ProfileForm(instance=user)
        patient_form = PatientForm(instance=patient) if patient else None
    return render(request, 'edit_user.html', {'form': form, 'patient_form': patient_form, 'user': user})

@login_required
def delete_user(request, user_id):
    if not (request.user.is_superuser):
        return redirect('home')

    user = get_object_or_404(RendeloUser, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('admin_view')
    return render(request, 'delete_user.html', {'user': user})

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
            send_mail(
                'Sikeres regisztráció!',
                'Kedves {},\n\nSikeresen regisztrált a rendszerünkbe, köszönjük, hogy klinikánkat választotta!\n\nMostantól minden időpontot a fiókjában le tud foglalni, és orvosaink is látni fogják a kezelési előzményeit.\n\nÜdvözlettel,\nMosolyfogaszat.hu'.format(user.username),
                'your_email@example.com',
                [user.email],
                fail_silently=False,
                )
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
    patient_form = None
    doctor_form = None

    if user.is_superuser:
        patient_form = None
    elif user.is_staff:
        doctor = get_object_or_404(Doctor, id=user.id)
        doctor_form = DoctorForm(request.POST or None, request.FILES or None, instance=doctor)
    else:
        try:
            patient = get_object_or_404(Patient, id=user.id)
            patient_form = PatientForm(request.POST or None, instance=patient)
        except Patient.DoesNotExist:
            patient_form = None

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data['password1']:
                user.set_password(form.cleaned_data['password1'])
            user.save()
            if patient_form and patient_form.is_valid():
                patient_form.save()
            if doctor_form and doctor_form.is_valid():
                doctor_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "A profilja sikeresen frissítve lett.")
            logger.info("Profile updated successfully")
            return redirect('profile')
        else:
            logger.error("Profile form is not valid: %s", form.errors)
    else:
        form = ProfileForm(instance=user)

    appointments = Appointment.objects.filter(patient=user.id, status='booked').select_related('paymentstatus').order_by('-start') if not user.is_superuser and not hasattr(user, 'doctor') else None
    now = timezone.now()
    return render(request, 'profile.html', {'form': form, 'patient_form': patient_form, 'doctor_form': doctor_form, 'appointments': appointments, 'now': now})

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user.id, status='booked')
    doctor = get_object_or_404(Doctor, id=appointment.practitioner_id)
    doctoruser = get_object_or_404(RendeloUser, id=appointment.practitioner_id)
    treatment = get_object_or_404(Treatment, id=appointment.treatment_id)
    patient = get_object_or_404(Patient, id=request.user.id)

    if request.method == 'POST':
        appointment.delete()

        send_mail(
            'Időpont törlése',
            f'Kedves {request.user.username},\n\nAz alábbi időpontot töröltük:\n\nKezelés: {treatment.name}\nIdőpont: {appointment.start.strftime("%Y-%m-%d %H:%M")}\nOrvos: {doctor.name}\n\nÜdvözlettel,\nMosolyfogaszat.hu',
            'your_email@example.com',
            [request.user.email],
            fail_silently=False,
        )

        send_mail(
            'Időpont törlése',
            f'Kedves {doctor.name},\n\nAz alábbi időpontot töröltük:\n\nPáciens: {patient.name}\nKezelés: {treatment.name}\nIdőpont: {appointment.start.strftime("%Y-%m-%d %H:%M")}\nTelefonszám: {patient.telecom}\nEmail cím: {request.user.email}\n\nÜdvözlettel,\nMosolyfogaszat.hu',
            'your_email@example.com',
            [doctoruser.email],
            fail_silently=False,
        )

        return redirect('profile')
    
    return render(request, 'cancel_appointment.html', {'appointment': appointment})

def get_available_slots(request):
    doctor_id = request.GET.get('doctor')
    date = request.GET.get('date')
    treatment_id = request.GET.get('treatment')
    treatment = Treatment.objects.get(id=treatment_id)
    treatment_duration = treatment.duration.total_seconds() // 60

    # Felfelé kerekítés 15 perces intervallumokra
    treatment_duration = ((treatment_duration + 14) // 15) * 15

    working_hours = WorkingHours.objects.filter(doctor_id=doctor_id, date=date)
    slots = []

    for wh in working_hours:
        start_time = datetime.combine(wh.date, wh.start)
        end_time = datetime.combine(wh.date, wh.end)
        current_time = start_time

        while current_time + timedelta(minutes=treatment_duration) <= end_time:
            slot_end_time = current_time + timedelta(minutes=treatment_duration)
            is_available = not Appointment.objects.filter(
                practitioner_id=doctor_id,
                start__lt=slot_end_time,
                end__gt=current_time,
                status='booked'
            ).exists()
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

@login_required
def add_admin_user(request):
    if not (request.user.is_superuser):
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_superuser = True
            user.is_staff = True
            user.save()

            send_mail(
                'Admin fiók létrehozása',
                f'Kedves {user.username},\n\nAz admin fiókja sikeresen létrehozásra került.\n\nFelhasználónév: {user.username}\nEmail cím: {user.email}\nJelszó: {request.POST["password1"]}\n\nKérjük, hogy a biztonság érdekében változtassa meg a jelszavát a bejelentkezést követően.\n\nÜdvözlettel,\nMosolyfogaszat.hu',
                'your_email@example.com',
                [user.email],
                fail_silently=False,
            )

            return redirect('admin_view')
    else:
        form = CustomUserCreationForm()
    return render(request, 'add_admin_user.html', {'form': form})

@login_required
def patients_view(request):
    if not (request.user.is_staff and not request.user.is_superuser):
        return redirect('home')
    
    search_query = request.GET.get('search', '')
    if search_query:
        patients = Patient.objects.filter(name__icontains=search_query)
    else:
        patients = Patient.objects.all()
    
    if not patients.exists():
        no_results_message = f"Nincs találat a megadott névre: {search_query}"
    else:
        no_results_message = None
    
    return render(request, 'patients.html', {'patients': patients, 'no_results_message': no_results_message})

@login_required
def patient_detail_view(request, patient_id):
    if not (request.user.is_staff and not request.user.is_superuser):
        return redirect('home')
    
    patient = get_object_or_404(Patient, id=patient_id)
    appointments = Appointment.objects.filter(patient=patient_id).order_by('-start')
    
    month = request.GET.get('month')
    if month:
        year, month = map(int, month.split('-'))
        appointments = appointments.filter(start__year=year, start__month=month)
    
    return render(request, 'patient_detail.html', {'patient': patient, 'appointments': appointments})

@login_required
def appointments_today_view(request):
    if not (request.user.is_staff and not request.user.is_superuser):
        return redirect('home')
    
    doctor = get_object_or_404(Doctor, id=request.user.id)

    selected_date = request.GET.get('date', timezone.now().strftime('%Y-%m-%d'))
    appointments = Appointment.objects.filter(practitioner=doctor, start__date=selected_date, patient__isnull=False).order_by('start')
    
    for appointment in appointments:
        patient = get_object_or_404(Patient, id=appointment.patient)
        appointment.patient_name = patient.name
    
    return render(request, 'appointments_today.html', {'appointments': appointments, 'selected_date': selected_date})

@login_required
def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    patient = get_object_or_404(Patient, id=appointment.patient)
    treatment = get_object_or_404(Treatment, id=appointment.treatment.id)
    payment_status = get_object_or_404(PaymentStatus, appointment=appointment)
    
    if request.method == 'POST' and request.user.is_staff and not request.user.is_superuser:
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect(f'/appointments_today/?date={appointment.start.date().strftime("%Y-%m-%d")}')
    else:
        form = AppointmentForm(instance=appointment)
    
    return render(request, 'edit_appointment.html', {
        'appointment': appointment,
        'patient': patient,
        'treatment': treatment,
        'selected_date': appointment.start.date().strftime("%Y-%m-%d"),
        'payment_status': payment_status,
        'form': form
    })

@login_required
def working_hours_view(request):
    if not (request.user.is_staff and not request.user.is_superuser):
        return redirect('home')
    doctor = get_object_or_404(Doctor, id=request.user.id)
    selected_date_str = request.GET.get('date') or request.POST.get('date')
    if not selected_date_str:
        return render(request, 'working_hours.html', {'selected_date': None, 'no_working_hours': False, 'readonly': True})
    try:
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
    except ValueError:
        return HttpResponse("Érvénytelen dátum formátum.", status=400)
    try:
        instance = WorkingHours.objects.get(doctor=doctor, date=selected_date)
        no_working_hours = False
    except WorkingHours.DoesNotExist:
        instance = None
        no_working_hours = True
    readonly = selected_date <= datetime.now().date()
    if request.method == 'POST' and not readonly:
        form = WorkingHoursForm(request.POST, instance=instance)
        if form.is_valid():
            wh = form.save(commit=False)
            wh.doctor = doctor
            wh.date = selected_date
            wh.save()
            return redirect(f'/working_hours/?date={selected_date_str}')
    else:
        form = WorkingHoursForm(instance=instance)
    return render(request, 'working_hours.html', {'form': form, 'selected_date': selected_date_str, 'no_working_hours': no_working_hours, 'readonly': readonly, 'doctor': doctor})

@login_required
def delete_working_hours(request, date):
    if not (request.user.is_staff and not request.user.is_superuser):
        return redirect('home')
    doctor = get_object_or_404(Doctor, id=request.user.id)
    try:
        working_hours = WorkingHours.objects.get(doctor=doctor, date=date)
        working_hours.delete()
        return redirect(f'/working_hours/?date={date}')
    except WorkingHours.DoesNotExist:
        return redirect('working_hours')


@csrf_exempt
def payment_callback(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if data.get("status") in ["COMPLETED", "APPROVED"]:
                appointment = get_object_or_404(Appointment, id=data.get("orderRef"))
                payment_status, _ = PaymentStatus.objects.get_or_create(appointment=appointment)
                payment_status.is_paid = True
                payment_status.save()
                return JsonResponse({"message": "Fizetés sikeres"}, status=200)
            else:
                return JsonResponse({"message": "Fizetés sikertelen"}, status=400)
        except Exception as e:
            return HttpResponse("Hiba történt a fizetés feldolgozása során", status=500)
    return HttpResponse("Érvénytelen kérés", status=400)


