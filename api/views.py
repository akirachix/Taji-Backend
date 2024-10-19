import re
import json
import os
from google.oauth2 import service_account
import imghdr
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from google.cloud import vision_v1
from django.db.models import Q
from google.api_core.exceptions import GoogleAPIError
from image__upload.models import ImageUpload, DrugRecord
from pharmacies.models import Pharmacy
from recall_drugs.models import PPBData
from .serializers import ImageUploadSerializer
from .serializers import PPBDataSerializer, PharmacySerializer
from django.conf import settings
from user.models import User
import logging
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from datetime import timedelta  
from django.utils import timezone
from django.db.models import Count, Q 





logger = logging.getLogger(__name__)

MAX_IMAGE_SIZE = 5 * 1024 * 1024  

def is_valid_image(file):
    """Check if the image file is valid (JPEG, PNG, GIF)."""
    try:
        file_type = imghdr.what(file)
        return file_type in ['jpeg', 'png', 'gif']
    except Exception as e:
        logger.error(f"Error validating image: {str(e)}")
        return False

def is_valid_batch_format(batch_number):
    """
    Validate if the extracted text matches typical batch number formats.
    Typical formats include:
    - Alphanumeric string with 5-15 characters
    - Must contain at least one number
    - Must be preceded by batch/lot related keywords
    """
    if not batch_number or len(batch_number) < 5 or len(batch_number) > 15:
        return False
    
   
    if not any(char.isdigit() for char in batch_number):
        return False
    
    return True

def extract_batch_number_from_image(image_file):
    """Extract batch number from the image using Google Cloud Vision API."""
    try:
       
        image_file.seek(0)
        
        
        credentials_info = settings.GOOGLE_VISION_CREDENTIALS
        credentials = service_account.Credentials.from_service_account_info(credentials_info)
        client = vision_v1.ImageAnnotatorClient(credentials=credentials)

        
        image_content = image_file.read()
        image = vision_v1.Image(content=image_content)
        
        
        feature = vision_v1.Feature(type=vision_v1.Feature.Type.TEXT_DETECTION)
        request = vision_v1.AnnotateImageRequest(
            image=image,
            features=[feature]
        )

       
        response = client.annotate_image(request)

        if response.error.message:
            raise ValueError(f"Google Vision API error: {response.error.message}")

        
        texts = response.text_annotations
        if not texts:
            logger.warning("No text found in the image")
            raise ValueError("No text found in the image")

        extracted_text = texts[0].description

        
        patterns = [
            r"Batch\s*No\.?\s*[:.]?\s*([A-Z0-9]{5,15})",
            r"B\.?\s*No\.?\s*[:.]?\s*([A-Z0-9]{5,15})",
            r"Batch\s*Number\s*[:.]?\s*([A-Z0-9]{5,15})",
            r"Lot\s*No\.?\s*[:.]?\s*([A-Z0-9]{5,15})",
            r"Lot\s*Number\s*[:.]?\s*([A-Z0-9]{5,15})",
            r"L\.?\s*No\.?\s*[:.]?\s*([A-Z0-9]{5,15})",
            r"Control\s*No\.?\s*[:.]?\s*([A-Z0-9]{5,15})",
            r"Batch\s*ID\s*[:.]?\s*([A-Z0-9]{5,15})",
            r"(?:Batch|Lot)\s*[:.]?\s*([A-Z0-9]{5,15})"
            r"Control\s*No\.\s*(\d{5})", 
            r"Batch\s*Number:\s*(\d{4})", 
            r"Batch\s*No\.\s*:\s*(MHET/\d{4,5})",  
            r"Lot\s*&\s*Control\s*No\.\s*:\s*(\d{9}[A-Z0-9]{3})"
        ]

       
        for pattern in patterns:
            matches = re.findall(pattern, extracted_text, re.IGNORECASE)
            if matches:
                potential_batch = matches[0].strip()
                if is_valid_batch_format(potential_batch):
                    return potential_batch

       
        logger.warning("Text found but no valid batch number pattern matched")
        raise ValueError("No batch number found in the image")

    except GoogleAPIError as e:
        logger.error(f"Google API error: {str(e)}")
        raise ValueError(f"Google API error: {str(e)}")
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise ValueError(str(e))

class ImageUploadView(APIView):
    """View for uploading an image and extracting batch number from it."""

    def post(self, request, *args, **kwargs):
        try:
            
            image_file = request.FILES.get('image_file')
            if not image_file:
                return Response(
                    {"error": "No image file provided"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            if image_file.size > MAX_IMAGE_SIZE:
                return Response(
                    {"error": f"Image file is too large. Maximum size is {MAX_IMAGE_SIZE/1024/1024}MB"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )


            if not is_valid_image(image_file):
                return Response(
                    {"error": "Invalid image file type. Supported formats are JPEG, PNG, and GIF"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
               
                batch_number = extract_batch_number_from_image(image_file)
                
                
                ImageUpload.objects.create(image_file=image_file, batch_number=batch_number)

                
                ppb_record = PPBData.objects.filter(batch_number__iexact=batch_number).first()
                
                if ppb_record:
                    return Response({
                        "details": {
                            "batch_number": ppb_record.batch_number,
                            "drug_name": ppb_record.product_name,
                            "recall_date": ppb_record.recall_date,
                            "reason_for_recall": ppb_record.recall_reason,
                            "status":ppb_record.status
                        }
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "details": {
                                "The drug is safe to use."
                        }
                    }, status=status.HTTP_200_OK)

            except ValueError as e:
                error_message = str(e)
                if "No text found in the image" in error_message:
                    return Response({
                        "error": "Batch number not valid"
                    }, status=status.HTTP_404_NOT_FOUND)
                elif "No batch number found in the image" in error_message:
                    return Response({
                        "error": "Batch number not valid"
                    }, status=status.HTTP_404_NOT_FOUND)
                else:
                    raise e

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response(
                {"error": "An unexpected error occurred"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )




    def get(self, request):
        try:
            data = ImageUpload.objects.all().order_by('-uploaded_at')  
            serializer = ImageUploadSerializer(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving images: {str(e)}")
            return Response(
                {"error": "Failed to retrieve images"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )







class UploadStatusView(APIView):
    def get(self, request):
        now = timezone.now()

        
        uploads = ImageUpload.objects.aggregate(
            total_uploads=Count('id'),
            daily_uploads=Count('id', filter=Q(uploaded_at__date=now.date())),
            weekly_uploads=Count('id', filter=Q(uploaded_at__gte=now - timezone.timedelta(days=7))),
            monthly_uploads=Count('id', filter=Q(uploaded_at__month=now.month)),
            yearly_uploads=Count('id', filter=Q(uploaded_at__year=now.year)),
        )

        return Response(uploads, status=status.HTTP_200_OK)

    

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



class UserListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        logger.info("Retrieved user list.")
        return Response(serializer.data, status=status.HTTP_200_OK)
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            logger.error(f'User with ID {id} not found.')
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        logger.info(f'User with ID {id} retrieved successfully.')
        return Response(serializer.data)
    
class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            logger.info(f'User registered successfully: {user.email}')
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        logger.error(f'User registration failed: {serializer.errors}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



User = get_user_model()
class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            logger.info(f'Login attempt for non-existent user: {email}')
            return Response({
                'error': 'User does not exist',
                'signup_required': True
            }, status=status.HTTP_404_NOT_FOUND)
        django_user = authenticate(username=email, password=password)
        if django_user:
            logger.info(f'User logged in successfully: {email}')
            return Response({}, status=status.HTTP_200_OK)
        logger.error(f'Login failed for user: {email}')
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)




class ImageUploadStatusView(APIView):
    def get(self, request):
        recalled_numbers = request.query_params.getlist('recalled_numbers', [])
        now = timezone.now()

        uploads = {
            'daily': {
                'recalled_count': ImageUpload.objects.filter(
                    batch_number__in=recalled_numbers,
                    uploaded_at__date=now.date()
                ).count(),
                'non_recalled_count': ImageUpload.objects.exclude(
                    batch_number__in=recalled_numbers,
                    uploaded_at__date=now.date()
                ).count(),
            },
            'weekly': {
                'recalled_count': ImageUpload.objects.filter(
                    batch_number__in=recalled_numbers,
                    uploaded_at__gte=now - timezone.timedelta(weeks=1)
                ).count(),
                'non_recalled_count': ImageUpload.objects.exclude(
                    batch_number__in=recalled_numbers,
                    uploaded_at__gte=now - timezone.timedelta(weeks=1)
                ).count(),
            },
            'monthly': {
                'recalled_count': ImageUpload.objects.filter(
                    batch_number__in=recalled_numbers,
                    uploaded_at__gte=now - timezone.timedelta(days=30)
                ).count(),
                'non_recalled_count': ImageUpload.objects.exclude(
                    batch_number__in=recalled_numbers,
                    uploaded_at__gte=now - timezone.timedelta(days=30)
                ).count(),
            },
        }

        return Response(uploads, status=status.HTTP_200_OK)
