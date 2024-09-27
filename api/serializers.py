from rest_framework import serializers
from image__upload.models import ImageUpload,  DrugRecord
from pharmacies.models import Pharmacy
from recall_drugs.models import PPBData
from django.contrib.auth.models import User as DjangoUser
from user.models import User  # Adjust the import based on where your User model is located


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUpload
        fields = "__all__"
        

class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = '__all__'


class DrugRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugRecord
        fields = '__all__'


class PPBDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PPBData
        fields = "__all__"   

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password']
        read_only_fields = ['id']
    def create(self, validated_data):
        django_user = DjangoUser.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user = User.objects.create(
            user=django_user,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )
        return user

