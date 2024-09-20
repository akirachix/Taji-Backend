from django.db import models


# Create your models here.
class PPBData(models.Model):
    recall_date = models.DateField()
    recall_reference_number = models.CharField(max_length=100)
    product_name = models.CharField(max_length=255)
    inn_name = models.CharField(max_length=255)
    batch_number = models.CharField(max_length=255)
    manufacturer_name = models.CharField(max_length=255)
    recall_reason = models.TextField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.product_name} {self.batch_number} {self.recall_date} {self.recall_reference_number} {self.inn_name} {self.manufacturer_name} {self.recall_reason} {self.status}"