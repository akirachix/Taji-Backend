from rest_framework import serializers
from cron_jobs.models import PPBData

class PPBDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PPBData
        fields = "__all__"