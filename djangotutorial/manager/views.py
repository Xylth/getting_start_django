from email.policy import default
from traceback import print_tb
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Exists, OuterRef
from django.views.decorators.http import require_POST

from .forms import LoginForm, RegisterForm, ProfileForm, PasswordUpdateForm, StatusProfileForm
from .models import Application, UserApplication


@login_required
def homepage(request):
    apps = Application.objects.filter(
        userapplication__user=request.user,
        userapplication__status=True,
    )
    return render(request, "manager/homepage.html", {"apps": apps})

def login_user(request):
    default_form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, authenticate(request, username=form.cleaned_data["username"], password=form.cleaned_data["password"]))
            return redirect("manager:homepage")
        else:
            form.data = default_form.data.copy()
    else:
        form = default_form
    return render(request, "manager/login.html", {"form":form})

def register_user(request):
    default_form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("manager:homepage")
        else:
            form.data = default_form.data.copy()
    else:
        form = default_form
    return render(request, "manager/register.html", {"form":form})

@login_required
def logout_user(request):
    logout(request)
    return redirect("manager:login")

@login_required
def profile(request):
    user = User.objects.get(pk=request.user.pk)
    profile_form = ProfileForm(instance=user)
    password_update_form = PasswordUpdateForm()
    initial_profile = profile_form.initial   # avant toute validation
    status_profile_form = StatusProfileForm(instance=user)

    if request.method == "POST":
        if "update_profile" in request.POST:
            profile_form = ProfileForm(request.POST, instance=user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Profil mis à jour.")
                return redirect("manager:profile")
            profile_form.data = initial_profile
            messages.error(request, "Erreur lors de la mise à jour du profil.")

        elif "update_password" in request.POST:
            password_update_form = PasswordUpdateForm(request.POST, instance=user)
            if password_update_form.is_valid():
                user = password_update_form.save()
                update_session_auth_hash(request, user)  # évite la déconnexion
                messages.success(request, "Mot de passe mis à jour.")
                return redirect("manager:profile")
            messages.error(request, "Erreur lors de la mise à jour du mot de passe.")

    return render(request, "manager/profile.html", {
        "profile_form": profile_form,
        "password_update_form": password_update_form,
        "status_profile_form": status_profile_form,
    })


@login_required
def app_conf(request):
    active_for_user = UserApplication.objects.filter(
        application=OuterRef("pk"),
        user=request.user,
        status=True,
    )
    apps = Application.objects.annotate(activate=Exists(active_for_user))
    return render(request, "manager/app_conf.html", {"apps": apps})

@login_required
@require_POST
def toggle_app(request, app_id):
    app = get_object_or_404(Application, pk=app_id)
    link, _ = UserApplication.objects.get_or_create(user=request.user, application=app)
    link.status = not link.status
    link.save(update_fields=["status"])
    return redirect("manager:app_conf")