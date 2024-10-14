from os import terminal_size

from OpenSSL.rand import status
from django.template.defaultfilters import title
from django.utils.termcolors import RESET
from rest_framework import serializers

from apps.user.models import Seller, Comment
from core.settings.base import HOST
from apps.common.models import Customer, Location, Product, Sector, MedicalSector, Source, PaymentType, PaymentMethod, \
    SubLocation


class LocationShortSerializers(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name']


class SubLocationCreateSerializers(serializers.ModelSerializer):

    class Meta:
        model = SubLocation
        fields = ['id', 'name', 'location']

    def create(self, validated_data):
        user = self.context['request'].user

        if user.is_superuser:
            validated_data['status'] = True
            validated_data['seller'] = None
        else:
            seller = Seller.objects.filter(user=user, status='active').first()
            if not seller:
                raise serializers.ValidationError({"error": "Seller not found"})
            validated_data['status'] = False
            validated_data['seller'] = seller

        sub_location = SubLocation.objects.create(**validated_data)
        return sub_location


class SectorListCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = ['id', 'name', 'location']

    def create(self, validated_data):
        user = self.context['request'].user

        if user.is_superuser:
            validated_data['seller'] = None
            validated_data['status'] = True
        else:
            seller = Seller.objects.filter(user=user, status='active').first()
            if not seller:
                raise serializers.ValidationError({"error": "Seller not fount"})
            validated_data['seller'] = seller
            validated_data['status'] = False
        sector = Sector.objects.create(**validated_data)
        return sector
