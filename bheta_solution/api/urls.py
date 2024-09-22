from django.urls import path
from .views import PpbDataListView
from .views import (
    ImageUploadView,
    PharmacyListView,
    PharmacyDetailView,
)
from .pharmacy_views import get_nearby_pharmacies 

urlpatterns = [
    path('image-upload/', ImageUploadView.as_view(), name='image-upload'),
    path('pharmacies/', PharmacyListView.as_view(), name='pharmacy-list'),
    path('pharmacies/<int:id>/', PharmacyDetailView.as_view(), name='pharmacy-detail'),
    path('pharmacies/nearby/', get_nearby_pharmacies, name='get-nearby-pharmacies'),
    path("ppb-data/", PpbDataListView.as_view(), name='ppb-data-list'),
]
