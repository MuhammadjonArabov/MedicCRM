from OpenSSL.rand import status
from django.template.defaultfilters import title
from django.utils.termcolors import RESET
from rest_framework import serializers

from apps.user.models import Seller, Comment
from core.settings.base import HOST
from apps.common.models import Customer, Location, Product, Sector, MedicalSector, Source, PaymentType, PaymentMethod


class LocationShortSerializers(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name']
