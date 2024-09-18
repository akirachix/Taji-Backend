from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pharmacy.models import Pharmacy
from .serializers import PharmacySerializer
from upload_image.models import UploadImage
from .serializers import UploadImageSerializer
from rest_framework import generics


class PharmacyListView(APIView):
    def get(self, request):
        pharmacies = Pharmacy.objects.all()
        serializer = PharmacySerializer(pharmacies, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PharmacySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PharmacyDetailView(APIView):
    def get(self, request, pharmacy_id):
        pharmacy = Pharmacy.objects(Pharmacy, pharmacy_id=id)
        serializer = PharmacySerializer(pharmacy)
        return Response(serializer.data)
    
    def put(self, request, id):
        pharmacy = Pharmacy.objects(Pharmacy, pharmacy_id=id)
        serializer = PharmacySerializer(pharmacy, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pharmacy_id):
        pharmacy = Pharmacy.objects(Pharmacy, pharmacy_id=id)
        pharmacy.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UploadImageListView(APIView):
    def get(self, request):
        upload_image = UploadImage.objects.all()
        serializer = UploadImageSerializer(upload_image, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = UploadImageSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
class UploadImageDetailView(APIView):
    def get(self,request,id):
        upload_image = UploadImage.objects.get(id=id)
        serializer = UploadImageSerializer(upload_image)
        return Response(serializer.data)
    def put(self, request, id):
        upload_image = UploadImage.objects.get(id=id)
        serializer = UploadImageSerializer(upload_image, data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, id):
        upload_image = UploadImage.objects.get(id=id)
        upload_image.delete()
        return Response("Successfully deleted",status=status.HTTP_202_ACCEPTED)
class ImageUploadView(generics.CreateAPIView):
       queryset = UploadImage.objects.all()
       serializer_class = UploadImageSerializer


