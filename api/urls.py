from django.urls import path
from . import views

urlpatterns = [
    path("countries", views.search_countries),
    path("categories", views.search_categories),
    path("destination", views.search_destination),
    path("calculate", views.calculate_freight),
]
