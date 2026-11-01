from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, RegisterForm


@login_required
def homepage(request):
    return render(request, "manager/homepage.html")

def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, authenticate(request, username=form.cleaned_data["username"], password=form.cleaned_data["password"]))
            return redirect("manager:homepage")
    else:
        form = LoginForm()
    return render(request, "manager/login.html", {"form":form})

def register_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("manager:homepage")
    else:
        form = RegisterForm()
    return render(request, "manager/register.html", {"form":form})


def logout_user(request):
    logout(request)
    return redirect("manager:login")
