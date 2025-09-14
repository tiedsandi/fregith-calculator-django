from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from dashboard.models import Country, Category
import requests


@api_view(["GET"])
def search_countries(request):
    q = request.GET.get("search", "")
    countries = Country.objects.filter(country_name__icontains=q)
    results = [{"id": c.id, "country_name": c.country_name} for c in countries]
    return Response(results)


@api_view(["GET"])
def search_categories(request):
    country_id = request.GET.get("country_id")
    q = request.GET.get("search", "")
    categories = Category.objects.filter(
        country_id=country_id, category_title__icontains=q
    )
    results = [
        {
            "id": cat.id,
            "category_title": cat.category_title,
            "price_per_kilo": cat.price_per_kilo,
        }
        for cat in categories
    ]
    return Response(results)


@api_view(["GET"])
def search_destination(request):
    q = request.GET.get("search", "").strip()

    if not q:
        return Response(
            {
                "meta": {
                    "message": "Query search null",
                    "code": 400,
                    "status": "error",
                },
                "data": [],
            }
        )

    url = f"{settings.RAJA_ONGKIR_BASE_URL}/domestic-destination"
    headers = {"key": settings.RAJA_ONGKIR_API_KEY}
    params = {"search": q}

    try:
        r = requests.get(url, headers=headers, params=params, timeout=10)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        return Response(
            {"meta": {"message": str(e), "code": 500, "status": "error"}, "data": []},
            status=500,
        )

    data = r.json().get("data", [])

    results = [
        {
            "id": d["id"],
            "name": f"{d.get('subdistrict_name', '-')}, {d['district_name']}, "
            f"{d['city_name']}, {d['province_name']}. {d['zip_code']}",
        }
        for d in data[:20]
    ]

    return Response(results)
