from django import forms
from .models import RendeloUser, Patient, Treatment
from datetime import timedelta

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

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'gender', 'birthDate', 'telecom']
    
    name = forms.CharField(max_length=255, label='Név')
    gender = forms.ChoiceField(choices=[('male', 'Férfi'), ('female', 'Nő')], label='Nem')
    birthDate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Születési dátum')
    telecom = forms.CharField(max_length=255, label='Telefonszám', required=False)

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email cím')
    password = forms.CharField(widget=forms.PasswordInput, label='Jelszó')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = RendeloUser
        fields = ['username', 'email']
    
    username = forms.CharField(max_length=255, label='Felhasználónév')
    email = forms.EmailField(label='Email cím', widget=forms.EmailInput(attrs={'style': 'width: 100%;'}))

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
