# src/core/forms.py
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=150, label="Username")
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm password")
    first_name = forms.CharField(max_length=150, required=False, label="First name")
    last_name = forms.CharField(max_length=150, required=False, label="Last name")
    postal_code = forms.CharField(max_length=12, required=False, label="Postal code")
    date_of_birth = forms.DateField(
        label="Date of birth (YYYY-MM-DD)",
        help_text="Used to apply birthday benefits.",
        widget=forms.DateInput(attrs={"placeholder": "YYYY-MM-DD"})
    )

    def clean_username(self):
        u = self.cleaned_data["username"]
        if User.objects.filter(username=u).exists():
            raise ValidationError("Username already taken.")
        return u

    def clean_email(self):
        e = self.cleaned_data["email"].lower()
        if User.objects.filter(email=e).exists():
            raise ValidationError("Email already in use.")
        return e

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password1") != cleaned.get("password2"):
            raise ValidationError("Passwords do not match.")
        dob = cleaned.get("date_of_birth")
        if dob and dob > date.today():
            raise ValidationError("Date of birth cannot be in the future.")
        return cleaned
