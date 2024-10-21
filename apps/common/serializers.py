from lib2to3.fixes.fix_input import context

from redis.commands.search.reducers import random_sample
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from twisted.plugins.twisted_reactors import select

from apps.user.models import Seller, Comment, Notifications
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
        seller = Seller.objects.filter(user=user, status='active').first()

        if user.is_superuser:
            validated_data['status'] = True
            validated_data['seller'] = None
        else:
            if not seller:
                raise serializers.ValidationError({"errors": "Active seller not found!"})
            validated_data['seller'] = seller
            validated_data['status'] = False

        sub_location = SubLocation.objects.create(**validated_data)

        if seller:
            Notifications.objects.create(
                title="Yangi sub location yaratildi",
                text=f"Yangi sub location {seller} yaratdi",
                seller=seller,
                is_read=False,
                link=f"/sub-location/{sub_location.id}"
            )

        return sub_location


class SectorListCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = ['id', 'name', 'location']

    def create(self, validated_data):
        user = self.context['request'].user
        seller = Seller.objects.filter(user=user, status='active').first()

        if user.is_superuser:
            validated_data['seller'] = None
            validated_data['status'] = True
        else:
            if not seller:
                raise serializers.ValidationError("Active seller topilmadi!")
            validated_data['seller'] = seller
            validated_data['status'] = False
        sector = Sector.objects.create(**validated_data)

        if seller:
            Notifications.objects.create(
                title='Sector yaratildi',
                text=f'Sectorni {seller} yaratdi',
                seller=seller,
                is_read=False,
                link=f'/sector/{sector.id}'
            )
        return sector


class LocationListCreateSerializers(serializers.ModelSerializer):
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)

    class Meta:
        model = Location
        fields = ['id', 'name', 'latitude', 'longitude']

    def create(self, validated_data):
        user = self.context['request'].user
        seller = Seller.objects.filter(user=user, status='active').first()

        if user.is_superuser:
            validated_data['seller'] = None
            validated_data['status'] = True

        else:
            if not seller:
                raise serializers.ValidationError("Active seller topilmadi")
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
        seller = Seller.objects.filter(user=user, status='active').first()

        if user.is_superuser:
            validated_data['seller'] = None
            validated_data['status'] = True

        else:
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
        seller = Seller.objects.filter(user=user, status='active').first()

        if user.is_superuser:
            validated_data['seller'] = None
            validated_data['status'] = True  # 'satus' -> 'status'

        else:
            validated_data['seller'] = seller
            validated_data['status'] = False

        source = Source.objects.create(**validated_data)
        return source
