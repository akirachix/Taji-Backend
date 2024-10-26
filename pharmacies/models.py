from django.db import models
from .utils import geocode_address
from django.db.models import F
from geopy.distance import distance
from geopy.distance import geodesic
import requests




class Pharmacy(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    license_status = models.CharField(max_length=255)
    reported=models.BooleanField(max_length=100)

    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        if not self.latitude or not self.longitude:
            api_key = "AIzaSyBBYsZVdFOBv3is6gNS3SbHr_xWY4pkpV8"
            lat, lng = geocode_address(self.address, api_key)
            if lat and lng:
                self.latitude = lat
                self.longitude = lng
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


    def geocode_address(address, api_key):
     response = requests.get( f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}' ) 
     if response.status_code == 200: data = response.json() 
     if data['results']: 
        location = data['results'][0]['geometry']['location'] 
        return location['lat'], location['lng'] 
     return None, None    

    @staticmethod
    def get_nearby_pharmacies(user_latitude, user_longitude, radius_km=3):
        pharmacies = Pharmacy.objects.all()
        nearby_pharmacies = []
        user_location = (user_latitude, user_longitude)

        for pharmacy in pharmacies:
            pharmacy_location = (pharmacy.latitude, pharmacy.longitude)
            distance = geodesic(user_location, pharmacy_location).km
            if distance <= radius_km:
                nearby_pharmacies.append(pharmacy)

        return nearby_pharmacies

    @staticmethod
    def get_directions(origin_latitude, origin_longitude, destination_latitude, destination_longitude):
        origin = f"{origin_latitude},{origin_longitude}"
        destination = f"{destination_latitude},{destination_longitude}"
        return f"https://www.google.com/maps/dir/{origin}/{destination}"

    class Meta:
        verbose_name_plural = "Pharmacies"
