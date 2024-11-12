import json

from rest_framework import serializers
import re

from apps.common.models import Customer
from apps.user import models
from apps.user.models import User, Page, Seller, Notifications, Comment


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


class SellerLoginSerializers(serializers.ModelSerializer):
    phone = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('phone', 'password')

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')

        user = User.objects.filter(phone=phone).first()
        if not user:
            raise serializers.ValidationError({"error": "Siz ro'yxatdan o'tmagansiz"})

        if not user.check_password(password):
            raise serializers.ValidationError({"error": "Parol xato"})

        attrs['user'] = user
        return attrs


class CommentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ('id', 'status', 'text', 'audio', 'customer', 'seller', 'created_at', 'updated_at')


class SellerCoinsSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.SellerCoin
        fields = ('action', 'coins')


class SellerDetailSerializers(serializers.ModelSerializer):
    coins = SellerCoinsSerializers(many=True)

    class Meta:
        model = models.Seller
        fields = ('id', 'phone', 'full_name', 'image', 'coins')


class AdminDetailSerializers(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        fields = ('id', 'phone', 'full_name')

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class AdminUpdateSerializers(serializers.ModelSerializer):
    full_name = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'phone', 'full_name')

    def update(self, instance, validated_data):
        full_name = validated_data.pop('full_name', None)
        if full_name:
            name = full_name.split(' ', 1)
            instance.first_name = name[0]
            instance.last_name = name[1] if len(name) > 1 else ''
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance


class SellerVisitCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.SellerVisit
        fields = ['last_visit', 'visit_count']

    def create(self, validate_data):
        user = self.context['request'].user
        seller = Seller.objects.filter(user=user, status='active').first()

        seller_visit = models.SellerVisit.objects.create(
            seller=seller,
            last_visit=validate_data.get('last_visit'),
            visit_count=validate_data.get('visit_count', 0),
        )
        return seller_visit

    def update(self, instance, validate_data):
        user = self.context['request'].user
        seller = Seller.objects.filter(user=user, status='active').first()

        instance.seller = seller,
        instance.last_visit = validate_data.get('last_visit', instance.last_visit),
        instance.visit_count = validate_data.get('visit_count', instance.visit_count)
        instance.save()

        return instance

class PageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['id', 'name']

class AdminNotificationSerializers(serializers.ModelSerializer):
    text = serializers.CharField()
    title = serializers.CharField(max_length=255)
    seller =serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True
    )
    class Meta:
        model = Notifications
        fields = ['text', 'title', 'seller']



class CommentCreateSerializers(serializers.ModelSerializer):
    customer_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Comment
        fields = ['text', 'audio', 'file', 'customer_id']

    def create(self, validated_data):
        customer_id = validated_data.pop('customer_id')
        validated_data['customer'] = Customer.objects.get(id=customer_id)
        return super().create(validated_data)

    def validate(self, data):
        if not (data.get('text') or data.get('audio') or data.get('file')):
            raise serializers.ValidationError("Kamida bitta: 'text', 'audio', yoki 'file' maydonini to'ldiring.")
        return data

class SmsAdminCreateSerializers(serializers.Serializer):
    customer_ids = serializers.ListField(child=serializers.IntegerField(), allow_null=True, required=False)
    message = serializers.CharField(max_length=550, write_only=True, required=True,
                                    error_messages={
                                        "null": "Xabar bo'sh bo'lmaydi",
                                        "blank": "Xabar bo'sh bo'lmaydi"
                                    })
    title = serializers.CharField(max_length=225, write_only=True, required=False, allow_null=True)
    sending_at = serializers.DateTimeField(allow_null=True, required=False)
    status = serializers.CharField(required=True, error_messages={
        "null": "Kimga yuborishni belgilashingiz kerak",
        "blank": "Kimga yuborishni belgilashingiz kerak"
    })

    def create(self, validated_data):
        customer_ids = validated_data.get('customer_ids', [])
        message = validated_data.get('message')
        title = validated_data.get('title')
        sending_at = validated_data.get('sending_at')
        status = validated_data.get('status')

        if status and status != '':
            customer_send = Customer.objects.filter(status=status).exclude(id__in=customer_ids)
        else:
            customer_send = Customer.objects.exclude(id__in=customer_ids)

        if customer_ids.exists():
            sms_message = models.Sms.objects.create(
                title=title, message=message, sending_at=sending_at
            )
            sms_message.customers.set(customer_send)

            for customer in customer_send:
                pass

        return {
            "status": "SMS yuborilmoqda",
            "count": customer_send.count()
        }

class SellerUpdateSerializers(serializers.ModelSerializer):
    page_permissions = serializers.CharField(required=False, allow_null=True)
    password = serializers.CharField(required=False, write_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=models.User.objects.all(), required=False)

    class Meta:
        model = models.Seller
        fields = (
            "phone", "full_name", "image", "registered_address",
            "passport_img", "location_type", "personal_phone",
            "page_permissions", "status", "pinfl", "address",
            "password", "user", 'score'
        )

    def validate(self, value):
        try:
            page_permissions = json.load(value)
        except json.JSONDecodeError:
            raise serializers.ValidationError("page_permissions JSON formatda bo'lishi kerak")

        if not isinstance(page_permissions, list):
            raise serializers.ValidationError("page_permissions ro'yxat bo'lishi kerak")

        try:
            page_permissions = [int(item) for item in page_permissions]
        except ValueError:
            raise serializers.ValidationError("page_permissions faqat integer qiymatlari bo'lishi kerak.")

        return page_permissions