from django.urls import path, include
from . import views

urlpatterns = [
    path('sub-location/', views.SubLocationListCreateAPIView.as_view(), name='sub-location'),  # get or post
    path('sector/', views.SectorListCreateAPIView.as_view(), name='sector'),  # get or post
    path('location/', views.LocationListCreateAPIView.as_view(), name='location'),  # get or post
    path('medical-sector/', views.MedicalSectorListCreateAPIView.as_view(), name='medical-sector'),  # get or post
    path('source/', views.SourceListCreateAPIView.as_view(), name='source'),  # get or post

    path('location-name-list/', views.LocationNameListApiView.as_view(), name='location-name-list'),

]
