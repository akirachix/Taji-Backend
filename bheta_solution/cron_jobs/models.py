from django.db import models

class PPBData(models.Model):
    recall_date = models.DateField()
    drug_name = models.CharField(max_length=255)
    scientific_name = models.CharField(max_length=255)
    batch_number = models.CharField(max_length=255)
    manufacturer_name = models.CharField(max_length=255)
    recall_reason = models.TextField()
    
    def __str__(self):
        return self.drug_name