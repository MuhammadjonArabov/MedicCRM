from django.urls import path, include
from . import views

urlpatterns = [
    path('customer/', views.CustomerListCreateAPIView.as_view(), name='customer') # get or post

]
