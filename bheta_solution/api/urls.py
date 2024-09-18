from django.urls import path
from .views import PPBDataListView


urlpatterns = [
    path("ppb-data/", PPBDataListView.as_view(), name='ppb-data-list'),
]







