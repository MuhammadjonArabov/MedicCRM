from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Sector, SubLocation, Location, MedicalSector, PaymentType, PaymentMethod, Customer, Source, Product,
    StatusChangeRequest, Sale
)

def view_images(obj):
  return format_html('<img src="{}" height="60" />'.format(obj.image.url)) if obj.image else '-'

@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
  list_display = ['id', 'name', 'status']
  search_fields = ['name']
  list_filter = ['status']


@admin.register(SubLocation)
class SubLocationAdmin(admin.ModelAdmin):
  list_display = ['id', 'name', 'status', 'location']
  search_fields = ['name']
  list_filter = ['status', 'location']

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
  list_display = ['id', 'name', 'status', 'latitude', 'longitude']
  search_fields = ['name']
  list_filter = ['status']

@admin.register(MedicalSector)
class MedicalSectorAdmin(admin.ModelAdmin):
  list_display = ['id', 'name', 'status']
  search_fields = ['name']
  list_filter = ['status']

@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
  list_filter = ['id', 'name', 'image']

@admin.register(PaymentMethod)
class PaymentMethodeAdmin(admin.ModelAdmin):
  list_display = ['id', 'name', 'status']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
  list_display = ['id', 'name', 'copy_customer', 'seller', 'user', 'status' ]
  search_fields = ['name', 'extra_phone', 'telegram_phone', 'phone_number']
  list_filter = ['status', 'payment_type', 'payment_method']

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
  list_display = ['id', 'name', 'status', 'image']
  search_fields = ['name']
  list_filter = ['status']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
  list_display = ['id', 'name', 'image', 'status']
  search_fields = ['name']
  list_filter = ['status']

@admin.register(StatusChangeRequest)
class StatusChangeRequest(admin.ModelAdmin):
  list_display = ['id', 'type', 'comment', 'customer', 'seller', 'status', 'new_status', 'comment_status', 'sale']
  search_fields = ['text', 'comment__text', 'customer__phone_number', 'seller__phone']
  list_filter = ['type', 'status', 'new_status', 'comment_status']

