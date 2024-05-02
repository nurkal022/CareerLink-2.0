from django import forms
from .models import Candidate


class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ["biography", "image"]
        widgets = {
            "biography": forms.Textarea(attrs={"class": "form-control"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
        }


from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Пайдаланушы аты", max_length=150, help_text="150 таңбадан аспайды."
    )
    password1 = forms.CharField(
        label="Құпия сөз",
        widget=forms.PasswordInput,
        help_text="Құпия сөз кемінде 8 таңба болуы тиіс.",
    )
    password2 = forms.CharField(
        label="Құпия сөзді қайталаңыз",
        widget=forms.PasswordInput,
        help_text="Құпия сөздің дәлме-дәл сәйкес келуі қажет.",
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")


from django import forms
from django.contrib.auth.forms import AuthenticationForm


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Пайдаланушы аты")
    password = forms.CharField(label="Құпия сөз", widget=forms.PasswordInput)
