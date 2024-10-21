from django.db.models import Case, When, Value, IntegerField
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from . import serializers, models
from .veriabels import UZBEK_ALPHABET


class SubLocationListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.SubLocationCreateSerializers
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['location_id']
    search_fields = ['name']

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            queryset = models.SubLocation.objects.all().order_by('-created_at')

        else:
            queryset = models.SubLocation.objects.filter(status=True).order_by('-created_at')
            seller = models.Seller.objects.filter(user=user, status='active').first()

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


class SectorListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.SectorListCreateSerializers
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['location_id']
    search_fields = ['name']

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            queryset = models.Sector.objects.all().order_by("-created_at")

        else:
            queryset = models.Sector.objects.filter(status=True).order_by("-created_at")
            seller = models.Seller.objects.filter(user=user, status='active').first()

            if seller:
                seller_sector = models.Sector.objects.filter(seller=seller, status=False).order_by("-created_at")
                return seller_sector | queryset

        queryset = queryset.annotate(
            customer_order=Case(
                *[When(name__istartswith=letter, then=Value(i)) for i, letter in enumerate(UZBEK_ALPHABET)],
                default=Value(len(UZBEK_ALPHABET)),
                output_field=IntegerField()
            )
        ).order_by("customer_order", "-created_at")

        return queryset


class LocationListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.LocationListCreateSerializers
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            queryset = models.Location.objects.all().order_by("-created_at")

        else:
            queryset = models.Location.objects.filter(status=True).order_by("-created_at")
            seller = models.Seller.objects.filter(user=user, status='active').first()
            if seller:
                seller_location = models.Location.objects.filter(seller=seller, status=False).order_by("-created_at")
                return seller_location | queryset

        queryset = queryset.annotate(
            customer_order=Case(
                *[When(name__istartswith=letter, then=Value(i)) for i, letter in enumerate(UZBEK_ALPHABET)],
                default=Value(len(UZBEK_ALPHABET)),
                output_field=IntegerField()
            )
        ).order_by("customer_order", "-created_at")

        return queryset


class MedicalSectorListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.MedicalSectorListCreateSerializers
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['location_id', 'sector_id']
    search_fields = ['name']

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            queryset = models.MedicalSector.objects.all().order_by("-created_at")

        else:
            queryset = models.MedicalSector.objects.filter(status=True).order_by("-created_at")
            seller = models.Seller.objects.filter(user=user, status='active').first()
            if seller:
                seller_medical_sector = models.MedicalSector(seller=seller, status=False).order_by("-created_at")
                return seller_medical_sector | queryset

        queryset = queryset.annotate(
            customer_order=Case(
                *[When(name__istartswith=letter, then=Value(i)) for i, letter in enumerate(UZBEK_ALPHABET)],
                default=Value(len(UZBEK_ALPHABET)),
                output_field=IntegerField()
            )
        ).order_by("customer_order", "-created_at")

        return queryset


class SourceListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.Source.objects.filter(status=True).order_by("-created_at")
    serializer_class = serializers.SourceCreateSerializers
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        source = models.Source.objects.filter(status=True)

        source = source.annotate(
            custom_order=Case(
                *[When(name__istartswith=letter, then=Value(i)) for i, letter in enumerate(UZBEK_ALPHABET)],
                default=Value(len(UZBEK_ALPHABET)),
                output_field=IntegerField()
            )
        ).order_by('custom_order', '-created_at')

        return source

