from django import forms
from .models import RendeloUser

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = RendeloUser
        fields = ['name', 'email', 'mobile_number', 'password1', 'password2']
    
    name = forms.CharField(max_length=255, label='Név')
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
        return user

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
