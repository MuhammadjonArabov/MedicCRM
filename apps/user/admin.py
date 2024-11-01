from django.contrib import admin
from django.utils.html import format_html

from .models import (
    User, Seller, Comment, Notifications, SellerVisit, SellerPageVisitDuration, SellerButtonClick,
    SellerCoin, SellerCustomerView, Comment, Page, Sms
)


def view_image(obj):
    return format_html('<img src="{}" height="60" />'.format(obj.image.url)) if obj.image else '-'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone', 'is_superuser']
    search_fields = ['phone']
    list_filter = ['is_staff', 'is_superuser']


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'phone', 'full_name', 'image', 'personal_phone']
    search_fields = ['user', 'phone', 'personal_phone']
    list_filter = ['phone', 'personal_phone']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'text', 'customer', 'seller', 'user']
    search_fields = ['customer', 'seller']
    list_filter = ['status', 'customer', 'seller']

@admin.register(Notifications)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'text', 'seller', 'is_read']
    search_fields = ['title', 'seller']
    list_filter = ['is_read']
