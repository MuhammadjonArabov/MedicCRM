from django.contrib import admin
from django.utils.html import format_html

from .models import (
    User, Seller, Comment, Notifications, SellerPageVisitDuration,
    SellerButtonClick, SellerVisit, Calendar, SellerCoin, Sms,
    ConfirmSale, Page, SellerCustomerView
)


def view_image(obj):
    """Mahsulot rasmni ko'rsatish."""
    return format_html('<img src="{}" height="60" />'.format(obj.image.url)) if obj.image else '-'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'is_superuser')
    search_fields = ('phone',)
    list_filter = ('is_staff', 'is_superuser')


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'full_name', 'location_type', 'status', 'personal_phone'
    )
    search_fields = ('full_name', 'personal_phone')
    list_filter = ('location_type', 'status')

    def view_image(self, obj):
        """Mahsulot rasmni ko'rsatish."""
        return format_html('<img src="{}" height="60" />'.format(obj.image.url)) if obj.image else '-'

    view_image.short_description = 'Image'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'seller', 'status', 'text', 'audio', 'video')
    search_fields = ('text',)
    list_filter = ('status',)


@admin.register(Notifications)
class NotificationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'text', 'seller', 'is_read', 'link')
    search_fields = ('title', 'text')
    list_filter = ('is_read',)


@admin.register(SellerPageVisitDuration)
class SellerPageVisitDurationAdmin(admin.ModelAdmin):
    list_display = ('id', 'seller', 'page', 'duration')
    search_fields = ('seller__phone', 'page')
    list_filter = ('seller',)


@admin.register(SellerButtonClick)
class SellerButtonClickAdmin(admin.ModelAdmin):
    list_display = ('id', 'seller', 'page', 'date', 'count')
    search_fields = ('seller__phone', 'page__name')
    list_filter = ('date',)


@admin.register(SellerVisit)
class SellerVisitAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'last_visit', 'visit_count')
    search_fields = ('user__phone',)
    list_filter = ('last_visit',)


@admin.register(Calendar)
class CalendarAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'title', 'status', 'customer', 'seller', 'is_approved')
    search_fields = ('title', 'customer__phone', 'seller__phone')
    list_filter = ('status', 'is_approved')


@admin.register(SellerCoin)
class SellerCoinAdmin(admin.ModelAdmin):
    list_display = ('id', 'action', 'seller', 'coins')
    search_fields = ('seller__phone',)
    list_filter = ('action',)


@admin.register(Sms)
class SmsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'message', 'sent_at', 'view_sellers')
    search_fields = ('title', 'message')
    list_filter = ('sent_at',)

    def view_sellers(self, obj):
        return ", ".join([str(seller.phone) for seller in obj.sellers.all()])

    view_sellers.short_description = 'Sellers'


@admin.register(ConfirmSale)
class ConfirmSaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'seller_percentage')
    search_fields = ('customer__phone',)
    list_filter = ('customer',)


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SellerCustomerView)
class SellerCustomerViewAdmin(admin.ModelAdmin):
    list_display = ('id', 'seller', 'customer', 'viewed_at')
    search_fields = ('seller__phone', 'customer__phone')
    list_filter = ('viewed_at',)

