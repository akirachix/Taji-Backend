from django.test import TestCase
from .models import Pharmacy
from django.core.exceptions import ValidationError

class PharmacyModelTest(TestCase):
    
    def setUp(self):
        self.pharmacy = Pharmacy.objects.create(
            name="Test Pharmacy",
            address="123 Test St",
            latitude=12.34,
            longitude=56.78,
            license_status="Active",
            reported=False
        )

    def test_pharmacy_creation(self):
        self.assertIsInstance(self.pharmacy, Pharmacy)
        self.assertEqual(self.pharmacy.name, "Test Pharmacy")
        self.assertEqual(self.pharmacy.address, "123 Test St")
        self.assertEqual(self.pharmacy.latitude, 12.34)
        self.assertEqual(self.pharmacy.longitude, 56.78)
        self.assertEqual(self.pharmacy.license_status, "Active")
        self.assertFalse(self.pharmacy.reported)

    def test_pharmacy_latitude_longitude_null(self):
        pharmacy = Pharmacy.objects.create(
            name="Another Pharmacy",
            address="456 Another St",
            license_status="Inactive",
            reported=True
        )
        self.assertIsNone(pharmacy.latitude)
        self.assertIsNone(pharmacy.longitude)

    def test_pharmacy_license_status(self):
        pharmacy = Pharmacy.objects.create(
            name="Third Pharmacy",
            address="789 Third St",
            latitude=98.76,
            longitude=54.32,
            license_status="Pending",
            reported=False
        )
        self.assertEqual(pharmacy.license_status, "Pending")

    def test_pharmacy_reported_field(self):
        pharmacy = Pharmacy.objects.create(
            name="Fourth Pharmacy",
            address="101 Fourth St",
            latitude=11.11,
            longitude=22.22,
            license_status="Active",
            reported=True
        )
        self.assertTrue(pharmacy.reported)

    def test_pharmacy_name_max_length(self):
        long_name = "A" * 256  # Exceeding max length
        with self.assertRaises(ValidationError):
            pharmacy = Pharmacy(name=long_name, address="123 Test St", license_status="Active", reported=False)
            pharmacy.full_clean()  # This will trigger validation

    def test_pharmacy_address_max_length(self):
        long_address = "B" * 256  # Exceeding max length
        with self.assertRaises(ValidationError):
            pharmacy = Pharmacy(name="Valid Name", address=long_address, license_status="Inactive", reported=True)
            pharmacy.full_clean()  # This will trigger validation
