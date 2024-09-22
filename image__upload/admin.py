from django.contrib import admin
from .models import ImageUpload, DrugRecord

@admin.register(ImageUpload)
class ImageUploadAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_file', 'uploaded_at']
    search_fields = ['image_file']

@admin.register(DrugRecord)
class DrugRecordAdmin(admin.ModelAdmin):
    list_display = ['batch_number', 'drug_name', 'recall_date']
    search_fields = ['batch_number', 'drug_name']
