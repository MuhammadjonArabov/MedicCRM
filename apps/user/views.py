from OpenSSL.rand import status
from django.template.context_processors import request
from django.utils.datetime_safe import datetime
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.user.serializers import UserSellerCreateSerializers
from rest_framework import generics
from apps.user.models import Seller, User


class SellerCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSellerCreateSerializers

    def get_queryset(self):
        return Seller.objects.none()


class SellerLoginAPIView(APIView):

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        password = request.data.get('password')

        if not phone or not password:
            return Response({'phone': 'Phone va password maydonlari majbury'}, status=400)

        user = User.objects.filter(phone=phone).first()
        if not user:
            raise ValidationError({"error": "Siz ro'yxatdan o'tmagansiz"}, code=400)

        if not user.check_password(password):
            return Response({'msg': 'Siz kiritgan parol xato iltimos qaytadan kiriting'}, status=400)

        user.last_login = datetime.now()
        user.save()

        seller = Seller.objects.filter(user=user, status="active").first()
        page_permissions = [page.name for page in seller.page_permissions.all()] if seller else []
        role = "admin" if user.is_superuser else "seller"

        data = {
            'role': role,
            'permissions': page_permissions,
            'msg': "Xush kelibsiz",
        }
        data.update(user.tokens())
        return Response(data, status=200)
