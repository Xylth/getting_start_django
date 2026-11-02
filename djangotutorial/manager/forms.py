from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from core.widgets import TogglePassInput


class LoginForm(forms.Form):
    username = forms.CharField(label="Identifiant")
    password = forms.CharField(label="Mot de passe", widget=TogglePassInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                self.add_error("password", "Identifiant ou mot de passe incorrect.")
        return cleaned_data


class RegisterForm(forms.ModelForm):
    password_confirm = forms.CharField(label="Confirmer mot de passe", widget=TogglePassInput)

    class Meta:
        model = User
        fields = ["username", "password"]
        labels = {"username": "Identifiant", "password": "Mot de passe"}
        widgets = {"password": TogglePassInput}

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

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
        labels = {"username": "Identifiant","first_name":"Prénom","last_name":"Nom","email":"Email"}

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

class PasswordUpdateForm(forms.ModelForm):
    new_password = forms.CharField(label="Nouveau mot de passe", widget=TogglePassInput)
    password_confirm = forms.CharField(label="Confirmer mot de passe", widget=TogglePassInput)

    class Meta:
        model = User
        fields = ["password"]
        labels = {"password": "Ancien mot de passe"}
        widgets = {"password": TogglePassInput}

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        new_password = cleaned_data.get("new_password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and not self.instance.check_password(password):
            self.add_error("password", "Mot de passe actuel incorrect.")

        if new_password and password_confirm and new_password != password_confirm:
            self.add_error("password_confirm", "Les mots de passe ne correspondent pas.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["new_password"])
        if commit:
            user.save()
        return user

class StatusProfileForm(forms.ModelForm):
    status = forms.CharField(label="Status",disabled=True)
    role = forms.CharField(label="Rôle",disabled=True)

    class Meta:
        model = User
        fields = ["date_joined","last_login"]
        labels = {"date_joined":"Date d'inscription","last_login":"Dernière connexion"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.instance
        self.fields["status"].initial = "● Actif" if user.is_active else "○ Inactif"
        self.fields["role"].initial = "Superuser" if user.is_superuser else "Utilisateur"

        # Affichage seul pour les dates aussi
        for name in ("date_joined", "last_login"):
            self.fields[name].disabled = True