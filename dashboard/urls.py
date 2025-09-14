from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("", views.dashboard_home, name="dashboard_home"),
    path("countries/", views.country_list, name="country_list"),
    path("countries/add/", views.country_create, name="country_add"),
    path("countries/<int:pk>/edit/", views.country_edit, name="country_edit"),
    path("countries/<int:pk>/delete/", views.country_delete, name="country_delete"),
    path("categories/", views.category_list, name="category_list"),
    path("categories/add/", views.category_create, name="category_add"),
    path("categories/<int:pk>/edit/", views.category_edit, name="category_edit"),
    path("categories/<int:pk>/delete/", views.category_delete, name="category_delete"),
]
