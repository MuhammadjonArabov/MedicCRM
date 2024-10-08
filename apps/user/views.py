from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q
from django.http import Http404
from rest_framework.exceptions import ValidationError
from django.utils.datetime_safe import datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.common.permissions import IsAdminUser, IsSellerUser
from apps.user import models
from apps.user import serializers
from rest_framework import generics
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class SellerCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.UserSellerCreateSerializers

    def get_queryset(self):
        return models.Seller.objects.none()


class SellerLoginAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = serializers.SellerLoginSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        user.last_login = datetime.now()
        user.save()

        seller = models.Seller.objects.filter(user=user, status="active").first()
        page_permissions = [page.name for page in seller.page_permissions.all()] if seller else []
        role = "admin" if user.is_superuser else "seller"

        data = {
            'role': role,
            'permissions': page_permissions,
            'msg': "Xush kelibsiz",
        }
        data.update(user.tokens())
        return Response(data)


class CommentAPIView(generics.ListAPIView):
    serializer_class = serializers.CommentsSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        seller_id = self.request.query_params.get('seller_id')
        customer_id = self.request.query_params.get('customer_id')

        if not seller_id or not customer_id:
            raise ValidationError("seller_id va customer_id parametirlari bo'lishi kerak")
        return models.Comment.objects.filter(seller_id=seller_id, customer_id=customer_id)


class UserDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        user = self.request.user
        if user.is_superuser:
            return serializers.AdminDetailSerializers
        else:
            return serializers.SellerDetailSerializers

    def get_object(self):
        user = self.request.user
        if user.is_superuser:
            return user
        else:
            models.Seller.objects.filter(user=user, status='active').first()


class AdminUpdateAPIView(generics.UpdateAPIView):
    serializer_class = serializers.AdminUpdateSerializers
    permission_classes = [IsAdminUser]
    http_method_names = ['patch']

    def get_object(self):
        user = self.request.user

        if not user.is_staff:
            raise PermissionDenied({"error": "Siz admin emassiz!"})

        return user


def notify_user(user_id, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user_id}",  # Group name
        {
            'type': 'send_notification',
            'message': message
        }
    )
