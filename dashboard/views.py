from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from .forms import (
    CustomUserCreationForm,
    CustomAuthenticationForm,
)
from django.contrib.auth.decorators import login_required


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect("dashboard_home")
    else:
        form = CustomUserCreationForm()
    return render(request, "dashboard/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard_home")
    else:
        form = CustomAuthenticationForm()
    return render(request, "dashboard/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def dashboard_home(request):
    return render(request, "dashboard/home.html")
