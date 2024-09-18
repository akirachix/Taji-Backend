from django.urls import path
from .views import PharmacyListView, PharmacyDetailView
from .views import UploadImageListView
from .views import UploadImageDetailView


urlpatterns = [
    path('api/pharmacies/', PharmacyListView.as_view(), name='pharmacy-list-view'),
    path('api/pharmacies/<int:id>/', PharmacyDetailView.as_view(), name='pharmacy-detail'),
    path('api/uploads_image/', UploadImageListView.as_view(), name='upload_image_list_view'),
    path('api/uploads_image/<int:id>/', UploadImageDetailView.as_view(), name='upload_image_detail_view'),
]
