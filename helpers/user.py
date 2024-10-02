from apps.user import models
from rest_framework.exceptions import PermissionDenied


def get_seller(user):
    seller = models.Seller.objects.filter(user=user, status='active').first()
    if not seller:
        raise PermissionDenied("Foydalanuvchi faol seller emas yoki seller topilmadi.")

    return seller
