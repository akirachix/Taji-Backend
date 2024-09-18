from django.db import models
class Pharmacy(models.Model):
    pharmacy_id = models.AutoField(primary_key=True)
    pharmacy_name = models.CharField(max_length=100)
    registration_number = models.PositiveSmallIntegerField()
    license_status = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.pharmacy_id} {self.pharmacy_name}"
# Create your models here.
