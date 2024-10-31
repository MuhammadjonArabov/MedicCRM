from datetime import datetime

from ckeditor.fields import RichTextField
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


phone_validator = RegexValidator(
    regex=r"^\+998\d{9}$", message=_("Telefon raqam noto'gri kiritildi"), code=403
)


class PhoneManager(BaseUserManager):
    use_in_migrations = True

    def normalize_phone(self, phone):
        return phone.strip()

    def _create_user(self, phone, email, password=None, **extra_fields):
        if not phone:
            raise ValueError("Telefon raqami kiritilishi shart")
        email = self.normalize_email(email)
        phone = self.normalize_phone(phone)
        user = self.model(phone=phone, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone, email, password, **extra_fields)

    def create_superuser(self, phone, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser bo'lishi uchun is_staff=True bo'lishi kerak.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser bo'lishi uchun is_superuser=True bo'lishi kerak.")

        return self._create_user(phone, email, password, **extra_fields)


class User(AbstractUser, BaseModel):
    phone = models.CharField(unique=True, validators=[phone_validator], max_length=50, blank=True)
    username = None
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
    )

    objects = PhoneManager()

    def save(self, *args, **kwargs):
        self.hashing_password()
        super().save(*args, **kwargs)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def hashing_password(self):
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)

    def __str__(self) -> str:
        return f"{str(self.id)}-{self.phone}"

    @property
    def active_seller(self):
        return self.sellers.filter(status='active').first()


class Seller(BaseModel):
    class LocationType(models.TextChoices):
        ONLINE = 'online', 'Online'
        OFFLINE = 'offline', 'Offline'
        HYBRID = 'hybrid', 'Hybrid'

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        DEACTIVATE = 'deactivate', 'Deactivate'
        ARCHIVED = 'archived', 'Archived'
        DELETED = 'deleted', 'Deleted'

    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='sellers', verbose_name=_('User'))
    phone = models.CharField(validators=[phone_validator], max_length=50, blank=True, null=True)
    full_name = models.CharField(max_length=255, verbose_name=_('Full name'))
    address = models.CharField(max_length=255, verbose_name=_('Address'))
    image = models.ImageField(upload_to='seller_images/', null=True, blank=True, verbose_name=_('Image'))
    registered_address = models.FileField(upload_to='registered_address/', null=True, blank=True,
                                          verbose_name=_('Registered Address'))
    add_customer_count = models.IntegerField(default=0, verbose_name=_('Add customer count'))
    pinfl = models.FileField(upload_to='pinfl/', null=True, blank=True, verbose_name=_('PINFL'))
    passport_img = models.ImageField(upload_to='passport_images/', null=True, blank=True,
                                     verbose_name=_('Passport Image'))
    location_type = models.CharField(max_length=10,
                                     choices=LocationType.choices, default=LocationType.OFFLINE)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.ACTIVE)
    personal_phone = models.CharField(max_length=50, validators=[phone_validator])
    page_permissions = models.ManyToManyField('Page', related_name='page', verbose_name=_('Page Permissions'), )

    def __str__(self):
        return f"{self.id}-{self.user}-{self.full_name}"

    def deactivate_other_sellers(self):
        Seller.objects.filter(user=self.user).exclude(id=self.id).update(status=self.Status.DEACTIVATE)

    def refresh_user_token(self):
        refresh_token = RefreshToken.for_user(self.user)
        refresh_token.blacklist()

    def save(self, *args, **kwargs):
        self.deactivate_other_sellers()

        if self.status in [self.Status.DEACTIVATE, self.Status.ARCHIVED, self.Status.DELETED]:
            self.phone = self.user.phone

        super().save(*args, **kwargs)

        self.refresh_user_token()


class Comment(BaseModel):
    status = models.BooleanField(default=True)
    text = RichTextField(null=True, blank=True, verbose_name=_('Text'))
    audio = models.FileField(upload_to='comments_audio/', null=True, blank=True, verbose_name=_('Audio'))
    file = models.FileField(upload_to='comments_files/', null=True, blank=True, verbose_name=_('File'))
    customer = models.ForeignKey('common.Customer', on_delete=models.CASCADE, related_name='customer_comments',
                                 verbose_name=_('Customer'))
    seller = models.ForeignKey('Seller', on_delete=models.CASCADE, related_name='seller_comments',
                               verbose_name=_('Seller'), null=True, blank=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_comments', verbose_name=_('User'),
                             null=True, blank=True)

    def __str__(self):
        return f"{str(self.id)}-{self.seller}-{self.customer}"


class Notifications(BaseModel):
    title = models.CharField(max_length=255, verbose_name=_('Title'), null=True, blank=True)
    text = RichTextField()
    seller = models.ForeignKey('Seller', on_delete=models.CASCADE, related_name='notifications',
                               verbose_name=_('Seller'))
    is_read = models.BooleanField(default=False)
    link = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Link'))

    def __str__(self):
        return str(self.title)


class SellerPageVisitDuration(BaseModel):
    seller = models.ForeignKey('Seller', on_delete=models.CASCADE, related_name='page_visit_durations',
                               verbose_name=_('Seller'))
    page = models.ForeignKey("Page", on_delete=models.CASCADE, related_name='visits', verbose_name=_('Page'))
    duration = models.PositiveIntegerField(verbose_name=_('Duration'))

    def __str__(self):
        return f"{self.seller} - {self.page}"


class SellerButtonClick(BaseModel):
    seller = models.ForeignKey('Seller', on_delete=models.CASCADE, related_name='seller_clicks',
                               verbose_name=_('Seller'))
    page = models.ForeignKey('Page', on_delete=models.CASCADE, related_name='page_clicks', verbose_name=_('Page'))
    date = models.DateField(verbose_name=_('Date'))
    count = models.IntegerField(default=0, verbose_name=_('Count'))

    def __str__(self):
        return f"{self.seller} - {self.page} - {self.date} - {self.count}"


class SellerVisit(BaseModel):
    seller = models.ForeignKey('Seller', on_delete=models.CASCADE, related_name='user_visits', verbose_name=_('User'))
    last_visit = models.DateTimeField(null=True, blank=True, verbose_name=_('Last Visit'))
    visit_count = models.FloatField(default=0, verbose_name=_('Visit Count'))

    def __str__(self):
        return f"{self.seller} - {self.last_visit}"


class Calendar(BaseModel):
    date = models.DateTimeField(verbose_name=_('Date'), null=True, blank=True)
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    status = models.BooleanField(default=False, verbose_name=_('Status'))
    customer = models.ForeignKey('common.Customer', on_delete=models.CASCADE, related_name='calendars',
                                 verbose_name=_('Customer'))
    seller = models.ForeignKey('Seller', on_delete=models.CASCADE, related_name='calendars', verbose_name=_('Seller'))
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.seller} - {self.date}"


class SellerCoin(BaseModel):
    class ActionType(models.TextChoices):
        ADD_CUSTOMER = 'add_customer', "Xaridor qo'shish"
        SALE = 'sale', "Sotuv"
        DO_ACTIVATION = 'do_activation', 'Foallashtirgan'

    action = models.CharField(max_length=50,
                              choices=ActionType.choices, default=ActionType.ADD_CUSTOMER)
    seller = models.ForeignKey('Seller', on_delete=models.CASCADE, related_name='seller_coins',
                               verbose_name=_('Seller'))
    coins = models.FloatField(verbose_name=_('Coins'))

    def __str__(self):
        return f"{self.seller} - {self.coins}"


class Sms(BaseModel):
    title = models.CharField(max_length=255, verbose_name=_('Title'), null=True, blank=True)
    message = models.TextField(verbose_name=_('Message'))
    sellers = models.ManyToManyField('Seller', related_name='sms_messages', verbose_name=_('Sellers'))
    sending_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Sending at'))
    customers = models.ManyToManyField('common.Customer', related_name='sms_customers', verbose_name=_('Customers'))

    def __str__(self):
        return f"{self.title} - {self.message}"


class Page(BaseModel):
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Page Name'))

    def __str__(self):
        return self.name


class SellerCustomerView(BaseModel):
    seller = models.ForeignKey('Seller', on_delete=models.CASCADE, related_name='customer_views', )
    customer = models.ForeignKey('common.Customer', on_delete=models.CASCADE, related_name='seller_customers', )
    count = models.BigIntegerField(default=0, verbose_name=_('Count'))
    viewed_at = models.DateTimeField(default=datetime.now, verbose_name=_('View At'))

    def __str__(self):
        return f"{self.seller} - {self.customer} - {self.viewed_at}"
