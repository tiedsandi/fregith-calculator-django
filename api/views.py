from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from dashboard.models import Country, Category
from .serializers import CountrySerializer, CategorySerializer
import requests


@api_view(["GET"])
def search_countries(request):
    q = request.GET.get("search", "")
    countries = Country.objects.filter(country_name__icontains=q)
    serializer = CountrySerializer(countries, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def search_categories(request):
    country_id = request.GET.get("country_id")
    q = request.GET.get("search", "")
    categories = Category.objects.filter(
        country_id=country_id, category_title__icontains=q
    )
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)
