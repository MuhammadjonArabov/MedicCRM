from lib2to3.fixes.fix_input import context
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from twisted.plugins.twisted_reactors import select

from apps.user.models import Seller, Comment
from apps.common.models import Customer, Location, Product, Sector, MedicalSector, Source, PaymentType, PaymentMethod, \
    SubLocation


class LocationShortSerializers(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name']


def get_activ_seller(seller):
    user = context['request'].user
    seller = Seller.objects.filter(user=user, status='active').first()
    if not seller:
        raise PermissionDenied("Active Seller not fount")
    return seller


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
            seller = get_activ_seller(user)
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
            seller = get_activ_seller(user)
            validated_data['seller'] = seller
            validated_data['status'] = False
        sector = Sector.objects.create(**validated_data)
        return sector


class LocationListCreateSerializers(serializers.ModelSerializer):
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)

    class Meta:
        model = Location
        fields = ['id', 'name', 'latitude', 'longitude']

    def create(self, validated_data):
        user = self.context['request'].user

        if user.is_superuser:
            validated_data['seller'] = None
            validated_data['status'] = True

        else:
            seller = get_activ_seller(user)
            validated_data['seller'] = seller
            validated_data['status'] = True

        location = Location.objects.create(**validated_data)
        return location


class MedicalSectorListCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = MedicalSector
        fields = ['id', 'name', 'inn_number', 'location', 'sector']

    def create(self, validated_data):
        user = self.context['request'].user

        if user.is_superuser:
            validated_data['seller'] = None
            validated_data['status'] = True

        else:
            seller = get_activ_seller(user)
            validated_data['seller'] = seller
            validated_data['status'] = False

        medical_sector = MedicalSector.objects.create(**validated_data)
        return medical_sector


class SourceCreateSerializers(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Source
        fields = ['id', 'name', 'image']

    def create(self, validated_data):
        user = self.context['request'].user

        if user.is_superuser:
            validated_data['seller'] = None
            validated_data['status'] = True  # 'satus' -> 'status'

        else:
            seller = get_activ_seller(user)
            validated_data['seller'] = seller
            validated_data['status'] = False

        source = Source.objects.create(**validated_data)
        return source





