from uuid import uuid4
from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import RendeloUser, Patient, Treatment, Doctor, WorkingHours, Appointment
from datetime import timedelta
from django.core.validators import RegexValidator

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = RendeloUser
        fields = ['username', 'email', 'password1', 'password2']
    
    username = forms.CharField(max_length=255, label='Felhasználónév')
    email = forms.EmailField(label='Email cím')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Jelszó')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Jelszó megerősítése')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("A két jelszó nem egyezik meg.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Jelszó')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Jelszó megerősítése')
    email = forms.EmailField(required=True)

    class Meta:
        model = RendeloUser
        fields = ('username', 'email', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("A két jelszó nem egyezik meg.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data["password1"])
        user.id = str(uuid4())  # Generate UUID
        if commit:
            user.save()
        return user

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'gender', 'birthDate', 'telecom']
    
    name = forms.CharField(max_length=255, label='Teljes név')
    gender = forms.ChoiceField(choices=[('male', 'Férfi'), ('female', 'Nő')], label='Nem')
    birthDate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Születési dátum')
    telecom = forms.CharField(max_length=255, label='Telefonszám', required=False)

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email cím')
    password = forms.CharField(widget=forms.PasswordInput, label='Jelszó')

class ProfileForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Új jelszó', required=False)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Új jelszó megerősítése', required=False)

    class Meta:
        model = RendeloUser
        fields = ['username', 'email', 'password1', 'password2']
    
    username = forms.CharField(
        max_length=255, 
        label='Felhasználónév',
        validators=[RegexValidator(
            regex=r'^[\w.@+\-_]+$', 
            message='Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.'
        )]
    )
    email = forms.EmailField(label='Email cím', widget=forms.EmailInput(attrs={'style': 'width: 100%;'}))

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("A két jelszó nem egyezik meg.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password1']:
            user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class TreatmentForm(forms.ModelForm):
    duration = forms.IntegerField(label='Időtartam (perc)', min_value=0)

    class Meta:
        model = Treatment
        fields = ['name', 'description', 'duration', 'price']
    
    name = forms.CharField(max_length=255, label='Név')
    description = forms.CharField(max_length=255, label='Leírás')
    price = forms.DecimalField(max_digits=10, decimal_places=0, label='Ár (forint)')

    def clean_duration(self):
        duration = self.cleaned_data['duration']
        return timedelta(minutes=duration)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.duration:
            self.initial['duration'] = int(self.instance.duration.total_seconds() // 60)

class CustomClearableFileInput(forms.ClearableFileInput):
    template_name = 'custom_clearable_file_input.html'

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'photo', 'qualification']

    name = forms.CharField(max_length=255, label='Név')
    photo = forms.ImageField(label='Fénykép', required=False, widget=CustomClearableFileInput)
    qualification = forms.CharField(max_length=255, label='Képesítés')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photo'].widget.attrs.update({'class': 'custom-file-input'})
        self.fields['photo'].label = 'Fénykép'
        self.fields['photo'].help_text = ''

class WorkingHoursForm(forms.ModelForm):
    class Meta:
        model = WorkingHours
        fields = [ 'start', 'end']
        widgets = {
            'start': forms.TimeInput(attrs={'type': 'time', 'step': 900, 'min': '08:00', 'max': '19:45', 'readonly': 'readonly'}),
            'end': forms.TimeInput(attrs={'type': 'time', 'step': 900, 'min': '08:15', 'max': '20:00', 'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start'].initial = '08:00'
        self.fields['end'].initial = '20:00'

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start')
        end = cleaned_data.get('end')
        if start and end and start >= end:
            raise forms.ValidationError("A kezdési időpont nem lehet későbbi vagy egyenlő a befejezési időponttal.")
        return cleaned_data
    
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['custom_description']
    
    custom_description = forms.CharField(widget=forms.Textarea, label='Leírás', required=False)
