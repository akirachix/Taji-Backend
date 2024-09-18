from rest_framework import serializers
from pharmacy.models import Pharmacy
from upload_image.models import UploadImage

class PharmacySerializer(serializers.ModelSerializer):
      class Meta:
            model =Pharmacy
            fields = "__all__"


class UploadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadImage
        fields = ['id','image']

