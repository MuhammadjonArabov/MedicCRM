from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Sector, SubLocation, Location, MedicalSector, Customer, Source, Product, StatusChangeRequest, PaymentMethod,
    PaymentType
)


def view_image(obj):
    """Mahsulot rasmni ko'rsatish."""
    return format_html('<img src="{}" height="60" />'.format(obj.image.url)) if obj.image else '-'


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status')
    search_fields = ('name',)
    list_filter = ('status',)


admin.site.register(PaymentMethod)
admin.site.register(PaymentType)


@admin.register(SubLocation)
class SubLocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'location')
    search_fields = ('name',)
    list_filter = ('status', 'location')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'latitude', 'longitude')
    search_fields = ('name',)
    list_filter = ('status',)


@admin.register(MedicalSector)
class MedicalSectorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status')
    search_fields = ('name',)
    list_filter = ('status',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'status', 'reactivate_data', 'extra_phone', 'seller', 'copy_customer')
    search_fields = ('phone_number', 'extra_phone', 'telegram_phone')
    list_filter = ('status', 'payment_type', 'payment_method')


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status')
    search_fields = ('name',)
    list_filter = ('status',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'view_image')
    search_fields = ('name',)
    readonly_fields = ('view_image',)

    def view_image(self, obj):
        return format_html('<img src="{}" height="60" />'.format(obj.image.url)) if obj.image else '-'


@admin.register(StatusChangeRequest)
class StatusChangeRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'comment', 'customer', 'seller', 'status', 'new_status', 'text')
    search_fields = ('text', 'comment__text', 'customer__phone_number', 'seller__phone')
    list_filter = ('type', 'status', 'new_status', 'comment_status')
