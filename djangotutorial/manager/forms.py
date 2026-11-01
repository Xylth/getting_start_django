from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label="Identifiant", max_length=150)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Identifiant ou mot de passe incorrect.")
        return cleaned_data


class RegisterForm(forms.ModelForm):
    password_confirm = forms.CharField(label="Confirmer mot de passe", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "password"]
        labels = {"username": "Identifiant", "password": "Mot de passe"}
        widgets = {"password": forms.PasswordInput()}

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", "Les mots de passe ne correspondent pas.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user