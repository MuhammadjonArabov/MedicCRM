from django.core.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError
from django.utils.datetime_safe import datetime
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import as_serializer_error
from rest_framework.views import APIView
from apps.common.permissions import IsAdminUser, IsSellerOrAdmin
from apps.user import models
from apps.user import serializers
from rest_framework import generics, status
from apps.common import models as common_models


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


class SellerVisitCreateAPIView(generics.CreateAPIView):
    queryset = models.SellerVisit.objects.all()
    serializer_class = serializers.SellerVisitCreateSerializers
    permission_classes = [IsAuthenticated, ]

    def get_seller_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class PageListAPIView(generics.ListAPIView):
    queryset = models.Page.objects.all()
    serializer_class = serializers.PageSerializers
    permission_classes = [IsSellerOrAdmin]


class AdminNotificationCreateAPIView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = serializers.AdminNotificationSerializers(data=request.data)

        if serializer.is_valid():
            validate_data = serializer.validated_data
            title = validate_data.get('title')
            text = validate_data.get('text')
            seller_ids = validate_data.get('seller')

            notifications = []

            for seller_id in seller_ids:
                try:
                    seller = models.Seller.objects.get(id=seller_id)
                except models.Seller.DoesNotExist:
                    raise ValidationError(f"Seller with ID {seller_id} does not exist.")

                notification = models.Notifications.objects.create(
                    title=title,
                    text=text,
                    seller=seller,
                    is_read=False,
                    link=None
                )
                notifications.append(notification)

            return Response(
                {'message': 'Notifications created successfully', 'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )


class CommentCreateAPIView(generics.CreateAPIView):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentCreateSerializers
    permission_classes = [IsAuthenticated]


class SmsAdminCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.SmsAdminCreateSerializers
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        return Response(result, 201)

class SellerUpdateAPIView(generics.UpdateAPIView):
    queryset = models.Seller.objects.filter(status='active')
    lookup_field = 'pk'
    serializer_class = serializers.SellerUpdateSerializers
    permission_classes = [IsAdminUser]