from django.contrib import admin
from django.utils.html import format_html

from .models import (
    User, Seller, Comment, Notifications, SellerVisit, SellerPageVisitDuration, SellerButtonClick,
    SellerCoin, SellerCustomerView, Comment, Page, Sms, Calendar
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

@admin.register(SellerPageVisitDuration)
class SellerPageVisitDurationAdmin(admin.ModelAdmin):
    list_display = ['id', 'seller', 'page', 'duration']
    search_fields = ['seller', 'page']
    list_filter = ['page']

@admin.register(SellerButtonClick)
class SellerButtonClickAdmin(admin.ModelAdmin):
    list_display = ['id', 'seller', 'date', 'count']
    search_fields = ['date', 'count']
    list_filter = ['date', 'count']

@admin.register(SellerVisit)
class SellerVisitAdmin(admin.ModelAdmin):
    list_display = ['id', 'seller', 'last_visit', 'visit_count']
    search_fields = ['last_visit', 'visit_count']
    list_filter = ['last_visit', 'visit_count']

@admin.register(Calendar)
class CalendarAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'title', 'status']
    search_fields = ['date', 'title']
    list_filter = ['status', 'is_approved']

@admin.register(SellerCoin)
class SellerCoinAdmin(admin.ModelAdmin):
    list_display = ['id', 'action', 'seller', 'coins']
    search_fields = ['seller', 'coins']
    list_filter = ['seller', 'coins']

@admin.register(Sms)
class SmsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'message', 'sending_at']
    search_fields = ['sending_at', 'title']
    list_filter = ['sending_at', 'sellers']

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(SellerCustomerView)
class SellerCustomerViewAdmin(admin.ModelAdmin):
    list_display = ['id', 'seller', 'customer', 'count']
    search_fields = ['count', 'viewed_at']
    list_filter = ['count', 'viewed_at']

