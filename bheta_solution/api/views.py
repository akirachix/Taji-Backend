from rest_framework import status
from cron_jobs.models import PPBData
from django.http import JsonResponse
from rest_framework.response import Response
from cron_jobs.models import PPBData
from .serializers import PPBDataSerializer
from rest_framework import generics



class PPBDataListView(generics.ListAPIView):
    queryset = PPBData.objects.all()
    serializer_class = PPBDataSerializer
class PPBDataListView(generics.ListAPIView):
    queryset = PPBData.objects.all()
    serializer_class = PPBDataSerializer
    def get(self, request):
        upload_image = PPBData.objects.all()
        serializer = PPBDataSerializer(upload_image, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = PPBDataSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    def ppb_data_list(request):
        if request.method == 'GET':
            data = list(PPBData.objects.all().values())
            return JsonResponse(data, safe=False)