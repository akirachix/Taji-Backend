from rest_framework import serializers
from image__upload.models import ImageUpload,  DrugRecord
from pharmacies.models import Pharmacy
from recall_drugs.models import PPBData

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

