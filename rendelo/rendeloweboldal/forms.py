from django import forms
from .models import RendeloUser, Patient

class RegistrationForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female')], label='Nem')
    birthDate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Születési dátum')

    class Meta:
        model = RendeloUser
        fields = ['username', 'email', 'mobile_number', 'password1', 'password2', 'gender', 'birthDate']
    
    username = forms.CharField(max_length=255, label='Felhasználónév')
    email = forms.EmailField(label='Email cím')
    mobile_number = forms.CharField(max_length=11, label='Telefonszám')
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
            if not user.is_superuser:
                Patient.objects.create(
                    id=user.id,
                    name=user.username,
                    gender=self.cleaned_data['gender'],
                    birthDate=self.cleaned_data['birthDate'],
                    telecom=user.mobile_number
                )
        return user

class LoginForm(forms.Form):
    email = forms.CharField(max_length=255, label='Email Cím')
    password = forms.CharField(widget=forms.PasswordInput, label='Jelszó')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = RendeloUser
        fields = ['username', 'email', 'mobile_number']
    
    username = forms.CharField(max_length=255, label='Felhasználónév')
    email = forms.EmailField(label='Email cím')
    mobile_number = forms.CharField(max_length=11, label='Telefonszám')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if RendeloUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ez az email cím már foglalt.")
        return email

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get('mobile_number')
        if RendeloUser.objects.filter(mobile_number=mobile_number).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ez a telefonszám már foglalt.")
        return mobile_number
