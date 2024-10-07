from django.urls import path

from . import views


urlpatterns = [
    path('seller-create/', views.SellerCreateAPIView.as_view(), name='seller-create'),
    path('seller-login/', views.SellerLoginAPIView.as_view(), name='seller-login'),
    path('comments/', views.CommentAPIView.as_view(), name='comments'),
    path('profile/', views.UserDetailAPIView.as_view(), name='user-profile'),
    path('admin-update/', views.AdminUpdateAPIView.as_view(), name='admin-update'),
    path('seller_dashport/', views.SellerDashportAPIView.as_view(), name='seller_dashport'),

]
