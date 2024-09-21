from django.test import TestCase
from unittest.mock import patch
from .models import ImageUpload, DrugRecord
from django.core.files.uploadedfile import SimpleUploadedFile
import datetime

class ImageUploadModelTest(TestCase):

    def test_imageupload_creation(self):
       
        image_file = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
       
        image_upload = ImageUpload.objects.create(
            image_file=image_file,
            batch_number="B12345"
        )        
        self.assertIn('uploads/test_image', image_upload.image_file.name)
        self.assertEqual(image_upload.batch_number, "B12345")
        self.assertIsNotNone(image_upload.uploaded_at)  



class DrugRecordModelTest(TestCase):

    def test_drugrecord_creation(self):
        drug_record = DrugRecord.objects.create(
            batch_number="B12345",
            drug_name="Test Drug",
            recall_status="Recalled",
            recall_date=datetime.date(2023, 9, 20),
            reason_for_recall="Contamination"
        )
        self.assertEqual(drug_record.batch_number, "B12345")
        self.assertEqual(drug_record.drug_name, "Test Drug")
        self.assertEqual(drug_record.recall_status, "Recalled")
        self.assertEqual(drug_record.recall_date, datetime.date(2023, 9, 20))
        self.assertEqual(drug_record.reason_for_recall, "Contamination")

    