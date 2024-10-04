from venv import create

from rest_framework import serializers
import re

from apps.user.models import User, Page, Seller


class UserSellerCreateSerializers(serializers.ModelSerializer):
    full_name = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True)
    image = serializers.ImageField(required=False)
    page_permissions = serializers.PrimaryKeyRelatedField(queryset=Page.objects.all(), many=True, required=False)

    class Meta:
        model = Seller
        fields = (
            'phone', 'full_name', 'password', 'image', 'page_permissions',
            'address', 'registered_address', 'pinfl', 'personal_phone', 'passport_img'
        )

    def validate_phone(self, value):
        uz_phone_regex = re.compile(r'^\+998\d{9}$')
        if not uz_phone_regex.match(value):
            raise serializers.ValidationError("Telefon raqam quyidagicha: +9989x xxx xx xx")
        return value

    def create_user(self, phone, password):
        return User.objects.create_user(phone=phone, password=password)

    def create_seller(self, user, validated_data):
        return Seller.objects.create(
            user=user,
            phone=validated_data.get('phone', ''),
            full_name=validated_data.get('full_name', ''),
            address=validated_data.get('address', ''),
            registered_address=validated_data.get('registered_address', ''),
            pinfl=validated_data.get('pinfl', ''),
            personal_phone=validated_data.get('personal_phone', ''),
            passport_img=validated_data.get('passport_img', ''),
            image=validated_data.get('image', ''),
        )

    def set_page_permissions(self, seller, page_permissions_ids):
        if page_permissions_ids:
            pages = Page.objects.filter(id__in=page_permissions_ids)
            seller.page_permissions.set(pages)

    def create(self, validated_data):
        phone = validated_data['phone']
        password = validated_data['password']
        user = User.objects.filter(phone=phone).first()

        if not user:
            user = self.create_user(phone, password)
        if password:
            user.set_password(password)
            user.save()

        page_permissions = validated_data.pop('page_permissions', [])

        seller = self.create_seller(user, validated_data)

        self.set_page_permissions(seller, page_permissions)

        return seller

        seller = self.create_seller(user, validated_data)
        self.set_page_permissions(seller, validated_data.get('page_permissions', []))

        return seller
