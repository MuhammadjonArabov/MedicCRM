from django.urls import path

from . import views


urlpatterns = [
    path('user/seller-create/', views.SellerCreateAPIView.as_view(), name='seller-create'),
    path('user/seller-login/', views.SellerLoginAPIView.as_view(), name='seller-login'),
    path('user/comments/', views.CommentAPIView.as_view(), name='seller-login'),

]
