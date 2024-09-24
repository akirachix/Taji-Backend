from django.db import models

      
class ImageUpload(models.Model):
    image_file = models.ImageField(upload_to='uploads/')
    batch_number = models.CharField(max_length=100, blank=True, null=True) 
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.image_file} (Batch: {self.batch_number})"  
  



class DrugRecord(models.Model): 
    batch_number = models.CharField(max_length=10, unique=True)
    drug_name = models.CharField(max_length=255)
    recall_status = models.CharField(max_length=50, default='Recalled')
    recall_date = models.DateField(null=True, blank=True)
    reason_for_recall = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.drug_name} (Batch: {self.batch_number})" 