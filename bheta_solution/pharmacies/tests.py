from django.test import TestCase
from unittest.mock import patch
from .models import Pharmacy


class PharmacyModelTest(TestCase):

    @patch('pharmacies.models.geocode_address')  
    def test_pharmacy_save_with_geocode(self, mock_geocode):
        mock_geocode.return_value = (1.234, 5.678)
        
        pharmacy = Pharmacy(name="Test Pharmacy", address="Test Address", license_status="Valid")
        pharmacy.save()

        self.assertEqual(pharmacy.latitude, 1.234)
        self.assertEqual(pharmacy.longitude, 5.678)
        mock_geocode.assert_called_once_with("Test Address", "AIzaSyBBYsZVdFOBv3is6gNS3SbHr_xWY4pkpV8")


    @patch('pharmacies.models.Pharmacy.get_nearby_pharmacies')
    def test_get_nearby_pharmacies(self, mock_get_nearby_pharmacies):
        mock_get_nearby_pharmacies.return_value = [
            Pharmacy(name="Pharmacy A", address="123 Street", latitude=-1.286389, longitude=36.817223),
            Pharmacy(name="Pharmacy B", address="456 Avenue", latitude=-1.2921, longitude=36.8219)
        ]

        pharmacies = Pharmacy.get_nearby_pharmacies(user_location=(-1.2921, 36.8219), radius_km=3)
        self.assertEqual(len(pharmacies), 2)
        self.assertEqual(pharmacies[0].name, "Pharmacy A")
        self.assertEqual(pharmacies[1].name, "Pharmacy B")
