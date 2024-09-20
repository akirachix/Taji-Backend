from django.urls import path
from .views import PpbDataListView



urlpatterns = [
    path("ppb-data/", PpbDataListView.as_view(), name='ppb-data-list'),
]