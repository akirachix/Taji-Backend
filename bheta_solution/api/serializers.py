from rest_framework import serializers
from image__upload.models import ImageUpload,  DrugRecord
from pharmacies.models import Pharmacy


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
