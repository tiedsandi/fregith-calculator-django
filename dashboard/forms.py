from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Country, Category


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)

    error_messages = {
        "password_mismatch": "The two password fields didn’t match.",
    }


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")
    error_messages = {"invalid_login": "Wrong password or email"}


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ["country_name", "country_flag", "country_currency"]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["country", "category_title", "price_per_kilo"]
