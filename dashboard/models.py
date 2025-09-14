from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Country(models.Model):
    country_name = models.CharField(max_length=100)
    country_flag = models.URLField(blank=True, null=True)
    country_currency = models.CharField(max_length=10)

    def __str__(self):
        return self.country_name


class Category(models.Model):
    country = models.ForeignKey(
        Country, related_name="categories", on_delete=models.CASCADE
    )
    category_title = models.CharField(max_length=200)
    price_per_kilo = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.category_title} ({self.country})"
