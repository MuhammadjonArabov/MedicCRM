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


class CustomerCreateSerializers(serializers.ModelSerializer):
    comment_text = serializers.CharField(
        write_only=True,
        read_only=False,
        allow_blank=True,
    )
    calendar_date = serializers.DateTimeField(
        write_only=True,
        required=False,
        allow_null=True,
    )
    products = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        many=True,
        required=True,
    )

    sector = serializers.PrimaryKeyRelatedField(
        queryset=Sector.objects.all(),
    )

    location = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(),
    )

    medical = serializers.PrimaryKeyRelatedField(
        queryset=MedicalSector.objects.all(),
    )

    source = serializers.PrimaryKeyRelatedField(
        queryset=Source.objects.all(),
    )

    payment_type = serializers.PrimaryKeyRelatedField(
        queryset=PaymentType.objects.all(),
        allow_null=True,
    )
    payment_method = serializers.PrimaryKeyRelatedField(
        queryset=PaymentMethod.objects.all(),
        allow_null=True,
    )

    class Meta:
        model = Customer
        fields = [
            'id', 'sector', 'location', 'medical', 'source', 'products',
            'name', 'payment_type', 'payment_method', 'extra_phone',
            'telegram_phone', 'phone_number', 'recall_date', 'comment_text',
            'calendar_date'
        ]

    def create(self, validated_data):
        comment_text = validated_data.pop('comment_text', None)
        calendar_date = validated_data.pop('calendar_date', None)

        user = self.context['request'].user
        seller = Seller.objects.get(user=user, status='active')  # `get()` dan foydalanamiz
        validated_data['seller'] = seller

        customer = super().create(validated_data)

        if comment_text:
            Comment.objects.create(
                customer=customer,
                seller=seller,
                text=comment_text,
            )
        if calendar_date:
            Customer.objects.create(
                customer=customer,
                seller=seller,
                date=calendar_date,
                title=comment_text,
                status=True,
                is_approved=False
            )
        return customer


class CustomerListSerializers(serializers.ModelSerializer):
    location = LocationShortSerializers()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Customer
        fields = ['id', 'phone_number', 'name', 'status', 'created_at', 'location']

    def get_seller_info(self, seller):
        if seller and seller.status == 'active':
            return {
                'id': seller.id,
                'image_url': f"{HOST}{seller.image.url}" if seller.image else "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png",
                'name': seller.name,
            }
        return None

    def get_all_seller(self, customer, user):
        sellers = []
        seller_info = self.get_seller_info(customer.seller)
        if seller_info:
            sellers.append(seller_info)

        if user.is_superuser:
            for copy in customer.copies.all():
                seller_info = self.get_seller_info(copy.seller)
                if seller_info:
                    sellers.append(seller_info)
        return sellers

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context['request']
        user = request.user
        original_customer = instance.copy_customer or instance

        if not instance.copy_customer:
            representation['copied_at'] = representation.pop('created_at')

        representation['seller'] = self.get_all_seller(original_customer, user)

        representation['name'] = representation.get('name', ' ')

        return representation
