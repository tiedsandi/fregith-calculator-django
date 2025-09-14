from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from .forms import (
    CustomUserCreationForm,
    CustomAuthenticationForm,
    CountryForm,
    CategoryForm,
)
from .models import Country, Category
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


@login_required
def country_list(request):
    countries = Country.objects.all()
    return render(request, "dashboard/country_list.html", {"countries": countries})


@login_required
def country_create(request):
    form = CountryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("country_list")
    return render(
        request, "dashboard/country_form.html", {"form": form, "title": "Add Country"}
    )


@login_required
def country_edit(request, pk):
    country = get_object_or_404(Country, pk=pk)
    form = CountryForm(request.POST or None, instance=country)
    if form.is_valid():
        form.save()
        return redirect("country_list")
    return render(
        request, "dashboard/country_form.html", {"form": form, "title": "Edit Country"}
    )


@login_required
def country_delete(request, pk):
    country = get_object_or_404(Country, pk=pk)
    if request.method == "POST":
        country.delete()
        return redirect("country_list")
    return render(
        request, "dashboard/country_confirm_delete.html", {"country": country}
    )


@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, "dashboard/category_list.html", {"categories": categories})


@login_required
def category_create(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("category_list")
    return render(
        request, "dashboard/category_form.html", {"form": form, "title": "Add Category"}
    )


@login_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect("category_list")
    return render(
        request,
        "dashboard/category_form.html",
        {"form": form, "title": "Edit Category"},
    )


@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        return redirect("category_list")
    return render(
        request, "dashboard/category_confirm_delete.html", {"category": category}
    )
