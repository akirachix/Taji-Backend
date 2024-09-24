from django.http import JsonResponse
from pharmacies.models import Pharmacy
from math import radians, sin, cos, sqrt, atan2



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
