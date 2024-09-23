from django.test import TestCase
from .models import ImageUpload, DrugRecord
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.utils import timezone

class ImageUploadModelTest(TestCase):

    def setUp(self):
        self.image_file = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'file_content',
            content_type='image/jpeg'
        )
        self.image_upload = ImageUpload.objects.create(
            image_file=self.image_file,
            batch_number="Batch001"
        )

    def test_image_upload_creation(self):
        self.assertIsInstance(self.image_upload, ImageUpload)
        self.assertEqual(self.image_upload.batch_number, "Batch001")
        self.assertIsNotNone(self.image_upload.uploaded_at)

    
    def test_image_upload_successful(self):
        self.assertTrue(self.image_upload.image_file.name.startswith('uploads/'))
        self.assertIn('test_image', self.image_upload.image_file.name)

class DrugRecordModelTest(TestCase):

    def setUp(self):
        self.drug_record = DrugRecord.objects.create(
            batch_number="BatchA123",
            drug_name="Aspirin",
            recall_status="Recalled",
            recall_date=None,
            reason_for_recall="Contaminated"
        )

    def test_drug_record_creation(self):
        self.assertIsInstance(self.drug_record, DrugRecord)
        self.assertEqual(self.drug_record.drug_name, "Aspirin")
        self.assertEqual(self.drug_record.recall_status, "Recalled")
        self.assertIsNone(self.drug_record.recall_date)

    def test_unique_batch_number(self):
        DrugRecord.objects.create(
            batch_number="BatchB123",  
            drug_name="Ibuprofen"
        )
        with self.assertRaises(ValidationError):
            drug_record = DrugRecord(batch_number="BatchA123", drug_name="Paracetamol")
            drug_record.full_clean()

    def test_drug_record_string_representation(self):
        self.assertEqual(str(self.drug_record), "Aspirin (Batch: BatchA123)")

    def test_drug_record_empty_batch_number(self):
        with self.assertRaises(ValidationError):
            drug_record = DrugRecord(batch_number="", drug_name="Paracetamol")
            drug_record.full_clean()

    def test_drug_record_long_drug_name(self):
        long_name = "A" * 256 
        with self.assertRaises(ValidationError):
            drug_record = DrugRecord(batch_number="BatchB456", drug_name=long_name)
            drug_record.full_clean()