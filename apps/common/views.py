from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from . import serializers, models
from apps.user.models import User


class SubLocationListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.SubLocationCreateSerializers
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['location_id']
    search_fields = ['name']

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return models.SubLocation.objects.all().order_by('-created_at')

        sub_location = models.SubLocation.objects.filter(status=True).order_by('-created_at')
        seller = User.objects.get_active_seller(user)

        if seller:
            seller_sub_location = models.SubLocation.objects.filter(seller=seller, status=False).order_by(
                '-created_at')
            return sub_location | seller_sub_location

        return sub_location


class SectorListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.SectorListCreateSerializers
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['location_id']
    search_fields = ['name']

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return models.Sector.objects.all().order_by('-created_at')

        sector = models.Sector.objects.filter(status=True).order_by('-created_at')
        seller = User.objects.get_active_seller(user)

        if seller:
            seller_sector = models.Sector.objects.filter(seller=seller, status=False).order_by(
                '-created_at')
            return sector | seller_sector

        return sector


class LocationListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.LocationListCreateSerializers
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return models.Location.objects.all().order_by('-created_at')

        location = models.Location.objects.filter(status=True).order_by('-created_at')
        seller = User.objects.get_active_seller(user)

        if seller:
            seller_location = models.Location.objects.filter(seller=seller, status=False).order_by(
                '-created_at')
            return location | seller_location

        return location


class MedicalSectorListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.MedicalSectorListCreateSerializers
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['location_id', 'sector_id']
    search_fields = ['name']

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return models.MedicalSector.objects.all().order_by('-created_at')

        medical_sector = models.MedicalSector.objects.filter(status=True).order_by('-created_at')
        seller = User.objects.get_active_seller(user)

        if seller:
            seller_medical_sector = models.MedicalSector.objects.filter(seller=seller, status=False).order_by(
                '-created_at')
            return medical_sector | seller_medical_sector

        return medical_sector


class SourceListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.Source.objects.filter(status=True).order_by("-created_at")
    serializer_class = serializers.SourceCreateSerializers
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        source = models.Source.objects.filter(status=True).order_by("-created_at")
        return source


class LocationNameListApiView(generics.ListAPIView):
    queryset = models.Location.objects.all()
    serializer_class = serializers.LocationNameListSerializers
    permission_classes = [IsAuthenticated]

