from django.utils.datetime_safe import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.user.serializers import UserSellerCreateSerializers, SellerLoginSerializers
from rest_framework import generics
from apps.user.models import Seller


class SellerCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSellerCreateSerializers

    def get_queryset(self):
        return Seller.objects.none()


class SellerLoginAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = SellerLoginSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        user.last_login = datetime.now()
        user.save()

        seller = Seller.objects.filter(user=user, status="active").first()
        page_permissions = [page.name for page in seller.page_permissions.all()] if seller else []
        role = "admin" if user.is_superuser else "seller"

        data = {
            'role': role,
            'permissions': page_permissions,
            'msg': "Xush kelibsiz",
        }
        data.update(user.tokens())
        return Response(data)