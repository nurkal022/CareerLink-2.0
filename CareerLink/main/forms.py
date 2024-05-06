from django import forms
from .models import *

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CustomUserEditForm(forms.ModelForm):
    username = forms.CharField(
        label=("Пайдаланушы аты"),
        max_length=150,
        help_text=(
            "150 таңбадан артық емес. Тек әріптер, сандар және @ / таңбалары./+/-/_ ."
        ),
        error_messages={
            "required": ("Бұл өріс міндетті болып табылады."),
            "invalid": ("Дұрыс пайдаланушы атын енгізіңіз."),
        },
    )

    class Meta:
        model = User
        fields = ["username", "email"]
        labels = {
            "username": ("Пайдаланушы аты"),
            "email": ("Электрондық пошта"),
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }


class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ["biography", "image"]
        labels = {"biography": "Өмірбаян", "image": "Сурет"}
        widgets = {
            "biography": forms.Textarea(attrs={"class": "form-control"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
        }


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


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ["name", "email", "message"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control border-0 py-3", "placeholder": "Аты-жөн"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control border-0 py-3", "placeholder": "Email"}
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "w-100 form-control border-0 py-3",
                    "rows": 6,
                    "placeholder": "Мәтін",
                }
            ),
        }
