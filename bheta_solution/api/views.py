# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from recall_drugs.models import PPBData
from .serializers import PPBDataSerializer



class PpbDataListView(APIView):
    
    def get(self, request):
        data = PPBData.objects.all() 
        serializer =PPBDataSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)