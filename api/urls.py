from django.urls import path
from .views import (
    ImageUploadView,
    PharmacyListView,
    PharmacyDetailView,
    PpbDataListView,
)
from .pharmacy_views import get_nearby_pharmacies 
from .views import UserListView, UserDetailView, RegisterView, LoginView
from .views import UploadStatusView
from .views import ImageUploadStatusView

urlpatterns = [
    path('image-upload/', ImageUploadView.as_view(), name='image-upload'),

    path('pharmacies/', PharmacyListView.as_view(), name='pharmacy-list'),
    path('pharmacies/<int:id>/', PharmacyDetailView.as_view(), name='pharmacy-detail'),
    path('pharmacies/nearby/', get_nearby_pharmacies, name='get-nearby-pharmacies'),

    path("ppb-data/", PpbDataListView.as_view(), name='ppb-data-list'),


    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:id>/', UserDetailView.as_view(), name='user-detail'),
    path('users/register/', RegisterView.as_view(), name='user-register'),
    path('users/login/', LoginView.as_view(), name='user-login'),

    path('upload-status/', UploadStatusView.as_view(), name='upload-status'),

    path('image-upload-status/', ImageUploadStatusView.as_view(), name='image-upload-status'),
]


