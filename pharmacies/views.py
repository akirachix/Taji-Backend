
from django.http import JsonResponse
from .models import Pharmacy
from math import radians, sin, cos, sqrt, atan2
import requests


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def get_nearby_pharmacies(request):
    user_lat = float(request.GET.get('lat'))
    user_lng = float(request.GET.get('lng'))
    
    nearby_pharmacies = []
    for pharmacy in Pharmacy.objects.all():
        distance = haversine(user_lat, user_lng, pharmacy.latitude, pharmacy.longitude)
        if distance <= 3:  
            nearby_pharmacies.append({
                'name': pharmacy.name,
                'address': pharmacy.address,
                'latitude': pharmacy.latitude,
                'longitude': pharmacy.longitude,
                'distance': distance,
            })

    return JsonResponse(nearby_pharmacies, safe=False)


def get_directions(start_lat, start_lng, end_lat, end_lng, api_key):
    endpoint = f"https://maps.googleapis.com/maps/api/directions/json?origin={start_lat},{start_lng}&destination={end_lat},{end_lng}&key={api_key}"
    response = requests.get(endpoint)
    if response.status_code == 200:
        return response.json()  
    else:
        raise Exception(f"Error with Google Directions API: {response.status_code}")


def get_pharmacy_directions(request, pharmacy_id):
    user_lat = float(request.GET.get('lat'))
    user_lng = float(request.GET.get('lng'))
    
    try:
        pharmacy = Pharmacy.objects.get(id=pharmacy_id)
        directions = get_directions(user_lat, user_lng, pharmacy.latitude, pharmacy.longitude, 'YOUR_GOOGLE_MAPS_API_KEY')
        return JsonResponse(directions, safe=False)
    except Pharmacy.DoesNotExist:
        return JsonResponse({'error': 'Pharmacy not found'}, status=404)
