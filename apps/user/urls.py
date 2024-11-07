from django.urls import path

from . import views


urlpatterns = [
    #POST
    path('seller-visit-create/', views.SellerVisitCreateAPIView.as_view(), name='seller-visit-create'),
    path('seller-create/', views.SellerCreateAPIView.as_view(), name='seller-create'),
    path('seller-login/', views.SellerLoginAPIView.as_view(), name='seller-login'),
    path('admin-notification/', views.AdminNotificationCreateAPIView.as_view(), name='admin-notification'),

    #GET
    path('comments/', views.CommentAPIView.as_view(), name='comments'),
    path('profile/', views.UserDetailAPIView.as_view(), name='user-profile'),
    path('page-list/', views.PageListAPIView.as_view(), name='page-list'),

    #PUT and PATCH
    path('admin-update/', views.AdminUpdateAPIView.as_view(), name='admin-update'),


]
