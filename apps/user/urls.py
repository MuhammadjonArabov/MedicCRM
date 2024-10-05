from django.urls import path

from . import views


urlpatterns = [
    path('seller-create/', views.SellerCreateAPIView.as_view(), name='seller-create'),
    path('seller-login/', views.SellerLoginAPIView.as_view(), name='seller-login'),

]
