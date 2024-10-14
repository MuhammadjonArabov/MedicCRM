from asyncio import open_unix_connection
from email.policy import default

from OpenSSL.rand import status
from PIL.ImageFilter import SMOOTH
from django.db.models import Case, When, Value, IntegerField
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from . import serializers, models

from apps.common.models import Customer
from .veriabels import UZBEK_ALPHABET
from ..user.models import Seller


class SubLocationListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.SubLocationCreateSerializers
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['location']
    search_fields = ['name']

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            queryset = models.SubLocation.objects.all().order_by('-created_at')

        else:
            queryset = models.SubLocation.objects.filter(status=True).order_by('-created_at')
            seller = Seller.objects.filter(status='active', user=user).first()

            if seller:
                seller_sub_location = models.SubLocation.objects.filter(seller=seller, status=False).order_by(
                    '-created_at')
                queryset = seller_sub_location | queryset

        queryset = queryset.annotate(
            customer_order=Case(
                *[When(name__istartswith=letter, then=Value(i)) for i, letter in enumerate(UZBEK_ALPHABET)],
                default=Value(len(UZBEK_ALPHABET)),
                output_field=IntegerField()
            )
        ).order_by("customer_order", "-created_at")

        return queryset
