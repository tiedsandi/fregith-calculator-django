from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny
from dashboard.models import Country, Category
from rest_framework.response import Response
from django.conf import settings
import requests


User = get_user_model()

@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def search_countries(request):
    q = request.GET.get("search", "")
    countries = Country.objects.filter(country_name__icontains=q)
    results = [
        {"id": c.id, "country_name": c.country_name, "flag": c.country_flag}
        for c in countries
    ]
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

    url = f"{settings.RAJA_ONGKIR_BASE_URL}destination/domestic-destination"
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


@api_view(["POST"])
def calculate_freight(request):
    data = request.data
    country_id = data.get("country_id")
    category_id = data.get("category_id")
    destination_id = data.get("destination_id")
    weight = data.get("weight")

    if not all([country_id, category_id, destination_id, weight]):
        return Response({"message": "Missing required fields"}, status=400)

    try:
        country_id = int(country_id)
        category_id = int(category_id)
        destination_id = int(destination_id)
        weight = int(weight)
    except (ValueError, TypeError):
        return Response({"message": "IDs dan weight harus angka"}, status=400)

    try:
        category = Category.objects.get(id=category_id, country_id=country_id)
    except Category.DoesNotExist:
        return Response({"message": "Category not found"}, status=404)

    origin = 17682

    payload_preview = {
        "origin": origin,
        "destination": destination_id,
        "weight": weight * 1000,
        "courier": "jne",
        "price": "lowest",
    }
    # print("Payload to be sent:", payload_preview)

    url = f"{settings.RAJA_ONGKIR_BASE_URL}calculate/domestic-cost"
    headers = {
        "key": settings.RAJA_ONGKIR_API_KEY,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    payload = payload_preview

    try:
        r = requests.post(url, data=payload, headers=headers, timeout=10)
        # print("Raw response:", r.text)
        r.raise_for_status()
        data = r.json().get("data", [])

        if data:
            domestic_price = data[0].get("cost", 0)
        else:
            domestic_price = 0

    except requests.exceptions.RequestException as e:
        print("RequestException:", str(e))
        if hasattr(e, "response") and e.response is not None:
            print("Response content:", e.response.text)
        domestic_price = 0

    international_price = weight * category.price_per_kilo
    total_price = international_price + domestic_price

    response_data = {
        "origin": origin,
        "destination": destination_id,
        "category_name": category.category_title,
        "international_price": international_price,
        "domestic_price": domestic_price,
        "total_price": total_price,
    }

    return Response(response_data)

@api_view(["POST"])
@permission_classes([AllowAny])
def register_api(request):
    email = request.data.get("email")
    password = request.data.get("password")
    confirm_password = request.data.get("confirm_password")

    if not email or not password or not confirm_password:
        return Response({"error": "Email, password, and confirm password required"}, status=400)

    if password != confirm_password:
        return Response({"error": "Passwords do not match"}, status=400)

    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already registered"}, status=400)

    user = User.objects.create(
        email=email,
        password=make_password(password),
    )
    token = AccessToken.for_user(user)
    return Response({"message": "Register success", "token": str(token)})

@api_view(["POST"])
@permission_classes([AllowAny])
def login_api(request):
    email = request.data.get("email")
    password = request.data.get("password")

    user = authenticate(request, email=email, password=password)
    if user is None:
        return Response({"error": "Invalid credentials"}, status=401)

    token = AccessToken.for_user(user)
    return Response({
        "token": str(token),
    })