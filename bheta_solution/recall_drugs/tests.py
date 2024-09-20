from django.test import TestCase
from .models import PPBData
from django.utils import timezone
from django.core.exceptions import ValidationError

class PPBDataModelTest(TestCase):

    def setUp(self):
       
        self.ppb_data = PPBData.objects.create(
            recall_date=timezone.now().date(),
            recall_reference_number='REF12345',
            product_name='Test Product',
            inn_name='Test INN',
            batch_number='BATCH123',
            manufacturer_name='Test Manufacturer',
            recall_reason='Test Recall Reason',
            status='active'
        )

    def test_ppb_data_creation(self):
       
        self.assertEqual(self.ppb_data.recall_reference_number, 'REF12345')
        self.assertEqual(self.ppb_data.product_name, 'Test Product')
        self.assertEqual(self.ppb_data.inn_name, 'Test INN')
        self.assertEqual(self.ppb_data.batch_number, 'BATCH123')
        self.assertEqual(self.ppb_data.manufacturer_name, 'Test Manufacturer')
        self.assertEqual(self.ppb_data.recall_reason, 'Test Recall Reason')
        self.assertEqual(self.ppb_data.status, 'active')

    def test_string_representation(self):
      
        expected_str = f"{self.ppb_data.product_name} {self.ppb_data.batch_number} {self.ppb_data.recall_date} {self.ppb_data.recall_reference_number} {self.ppb_data.inn_name} {self.ppb_data.manufacturer_name} {self.ppb_data.recall_reason} {self.ppb_data.status}"
        self.assertEqual(str(self.ppb_data), expected_str)

    def test_invalid_recall_date(self):
       
        with self.assertRaises(ValidationError):
            ppb_data_invalid = PPBData(
                recall_date='invalid-date',
                recall_reference_number='REF12345',
                product_name='Test Product',
                inn_name='Test INN',
                batch_number='BATCH123',
                manufacturer_name='Test Manufacturer',
                recall_reason='Test Recall Reason',
                status='active'
            )
            ppb_data_invalid.full_clean()  

    def test_empty_product_name(self):
     
        with self.assertRaises(ValidationError):
            ppb_data_invalid = PPBData(
                recall_date=timezone.now().date(),
                recall_reference_number='REF12345',
                product_name='',
                inn_name='Test INN',
                batch_number='BATCH123',
                manufacturer_name='Test Manufacturer',
                recall_reason='Test Recall Reason',
                status='active'
            )
            ppb_data_invalid.full_clean()  

    def test_max_length_exceeded(self):
       
        with self.assertRaises(ValidationError):
            ppb_data_invalid = PPBData(
                recall_date=timezone.now().date(),
                recall_reference_number='R' * 101, 
                product_name='Test Product',
                inn_name='Test INN',
                batch_number='BATCH123',
                manufacturer_name='Test Manufacturer',
                recall_reason='Test Recall Reason',
                status='active'
            )
            ppb_data_invalid.full_clean()  

    def test_recall_reason_not_empty(self):
        self.assertTrue(bool(self.ppb_data.recall_reason.strip()))
