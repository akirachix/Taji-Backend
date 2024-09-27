# Create your models here.
from django.db import models
from django.contrib.auth.models import User as DjangoUser


class User(models.Model):
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=16)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"