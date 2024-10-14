from django.urls import path, include
from . import views

urlpatterns = [
    path('sub-location/', views.SubLocationListCreateAPIView.as_view(), name='sub-location'), # get or post
    path('sector/', views.SectorListCreateAPIView.as_view(), name='sector'), # get or post

]
