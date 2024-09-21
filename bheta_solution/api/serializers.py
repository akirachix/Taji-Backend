from rest_framework import serializers
from recall_drugs.models import PPBData




class PPBDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PPBData
        fields = "__all__"   