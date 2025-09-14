from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from dashboard.models import Country
from .serializers import CountrySerializer
import requests


@api_view(["GET"])
def search_countries(request):
    q = request.GET.get("search", "")
    countries = Country.objects.filter(country_name__icontains=q)
    serializer = CountrySerializer(countries, many=True)
    return Response(serializer.data)
