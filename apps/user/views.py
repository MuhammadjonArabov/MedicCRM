from rest_framework.views import APIView
from apps.user.serializers import UserSellerCreateSerializers
from rest_framework import generics
from apps.user.models import Seller


class SellerCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSellerCreateSerializers

    def get_queryset(self):
        return Seller.objects.none()