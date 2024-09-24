

import re
import imghdr
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from google.cloud import vision
from django.db.models import Q
from google.api_core.exceptions import GoogleAPIError
from image__upload.models import ImageUpload, DrugRecord
from pharmacies.models import Pharmacy
from recall_drugs.models import PPBData
from .serializers import ImageUploadSerializer
from .serializers import PPBDataSerializer, PharmacySerializer

MAX_IMAGE_SIZE = 5 * 1024 * 1024 

def is_valid_image(file):
    """Check if the image file is valid (JPEG, PNG, GIF)."""
    file_type = imghdr.what(file)
    return file_type in ['jpeg', 'png', 'gif']

def extract_batch_number_from_image(image_file):
    """Extract batch number from the image using Google Cloud Vision API."""
    client = vision_v1.ImageAnnotatorClient()

    try:
        image_content = image_file.read()
        image = vision_v1.Image(content=image_content)
        feature = vision_v1.Feature(type=vision_v1.Feature.Type.TEXT_DETECTION)

        response = client.annotate_image({'image': image, 'features': [feature]})

        texts = response.text_annotations
        extracted_text = texts[0].description if texts else ""
    except GoogleAPIError as e:
        raise ValueError(f"Google API error: {str(e)}") from e
    except Exception as e:
        raise ValueError(f"Failed to process image: {str(e)}") from e

    patterns = [
        r"Batch No\.\s*(\d+)",
        r'B\.?\s*No\.?\s*:?\s*([A-Z0-9]+)', 
        r'Batch\s*No\.?\s*:?\s*([A-Z0-9]+)',
        r'B\.?\s*No\.?\s*([A-Z0-9]+)',
        r'([A-Z0-9]{5,10})',
        r'Batch\s*Code\s*:?\s*([A-Z0-9]+)',
        r'Lot\s*No\.?\s*:?\s*([A-Z0-9]+)',
        r'Lot\s*:?\s*([A-Z0-9]+)',
        r'L\.?\s*No\.?\s*:?\s*([A-Z0-9]+)',
        r'Lot\s*Code\s*:?\s*([A-Z0-9]+)',
        r'Batch\s*ID\s*:?\s*([A-Z0-9]+)',
        r'Batch\s*Number\s*:?\s*([A-Z0-9]+)',
        r'Control\s*No\.?\s*:?\s*([A-Z0-9]+)',
        r'B/N\s*:?\s*([A-Z0-9]+)',
        r'Lot/B\.?\s*No\.?\s*:?\s*([A-Z0-9]+)',
        r'Mfg\s*Batch\s*:?\s*([A-Z0-9]+)',
        r'Prod\s*Batch\s*:?\s*([A-Z0-9]+)',
        r'([A-Z]{2}[0-9]{3,6})',
        r'[B|L]atch\s*:?\s*([A-Z0-9]+)',
        r'BN\s*:?\s*([A-Z0-9]+)',
        r'Lot[\s/]*Batch\s*:?\s*([A-Z0-9]+)',
        r'[Bb]atch\s*#?\s*:?([A-Z0-9]+)',
        r'B\.?\s*No\.?\s*\.\s*([A-Z0-9]+)', 
        r'Lot\s*No\.?\s*:?\s*([0-9]+)', 
        r'Lot No\.\s*([0-9]{6})',  
    ]

    combined_pattern = r'|'.join(patterns)
    matches = re.findall(combined_pattern, extracted_text, re.IGNORECASE)
    return matches[0][0] if matches else None

class ImageUploadView(APIView):
    """View for uploading an image and extracting batch number from it."""

    def post(self, request, *args, **kwargs):
        image_file = request.FILES.get('image_file')

        if not image_file:
            return Response({"error": "No image file provided"}, status=status.HTTP_400_BAD_REQUEST)

        if image_file.size > MAX_IMAGE_SIZE:
            return Response({"error": "Image file is too large"}, status=status.HTTP_400_BAD_REQUEST)

        if not is_valid_image(image_file):
            return Response({"error": "Invalid image file type"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            batch_number = extract_batch_number_from_image(image_file)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        ImageUpload.objects.create(image_file=image_file)

        if batch_number:
            drug_record = DrugRecord.objects.filter(batch_number__iexact=batch_number.strip()).first()
            if drug_record:
                return Response({
                    "Batch_number": batch_number,
                    "Drug_name": drug_record.drug_name,
                    "Recall_status": "Recalled",
                    "Recall_date": drug_record.recall_date,
                    "Reason_for_Recall": drug_record.reason_for_recall,
                }, status=status.HTTP_200_OK)
            else:
                return Response({"message": "The drug is safe to use."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Batch number not valid"}, status=status.HTTP_404_NOT_FOUND)
        
    def get(self, request):
        data = ImageUpload.objects.all() 
        serializer = ImageUploadSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    

class PharmacyListView(APIView):
    
    def get(self, request):
        reported = request.query_params.get('reported')
        query = Q()
        if reported is not None:
            if reported.lower() == 'true':
                query &= Q(reported=True)
            elif reported.lower() == 'false':
                query &= Q(reported=False)
            
        pharmacies = Pharmacy.objects.filter(query)
        serializer = PharmacySerializer(pharmacies, many=True)
        return Response(serializer.data)



    def post(self, request):
        serializer = PharmacySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PharmacyDetailView(APIView):
    def get(self, request, id):
        pharmacy = get_object_or_404(Pharmacy, id=id)
        serializer = PharmacySerializer(pharmacy)

        user_lat = request.GET.get('user_lat')
        user_lng = request.GET.get('user_lng')

        if user_lat and user_lng:
            directions_url = f"https://www.google.com/maps/dir/?api=1&origin={user_lat},{user_lng}&destination={pharmacy.latitude},{pharmacy.longitude}&travelmode=driving"
        else:
            directions_url = None

        data = serializer.data
        data['directions_url'] = directions_url
        
        return Response(data)

class PpbDataListView(APIView):
    def get(self, request):
        data = PPBData.objects.all() 
        serializer = PPBDataSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
