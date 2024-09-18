from django.db import models

class UploadImage(models.Model):
    image = models.ImageField(upload_to='uploads/')
    def __str__(self):
        return f"{self.image}"

# Create your models here.
