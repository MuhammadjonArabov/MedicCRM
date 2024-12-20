from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from apps.user.models import Page


class IsAdminUser(BasePermission):

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise PermissionDenied('Foydalanuvchi authenticatedsiya qilinmagan yoki token mavjud emas')

        if not request.user.is_superuser:
            raise PermissionDenied('Foydalanuvhi admin emas')

        return True


class IsSellerUser(BasePermission):

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise PermissionDenied('Foydalanuvchi autentifikatsiyadan qilinmagan yoki token mavjud emas')

        if not request.user.sellers.exists():
            raise PermissionDenied('Foydalanuvchi seller emas yoki seller faol emas')

        return True


class IsSellerPage(BasePermission):

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise PermissionDenied('Foydalanuvchi authenticatedsiya qilinmagan yoki token mavjud emas')

        sellers = request.user.sellers(status='active')
        if not request.user.exists():
            raise PermissionDenied('Active seller topilmadi')

        seller = sellers.first()
        page_name = view.kwargs.get('page_name')

        try:
            page = Page.objects.get(name=page_name)
        except Page.DoesNotExist:
            raise PermissionDenied('Sahifa topilmadi')

        if page not in seller.page_permissions.all():
            raise PermissionDenied("Sahifaga ruxsat yo'q")

        return True


class IsSellerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise PermissionDenied('Foydalanuvchi authenticatedsiya qilinmagan yoki token mavjud emas')

        if not (request.user.is_superuser or request.user.sellers.filter(status='active').first()):
            raise PermissionDenied('Foydalanauvchi admin yoki active seller emas')

        return True
