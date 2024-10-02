import datetime

from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from apps.user.models import BaseModel


class Sector(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    status = models.BooleanField(default=False, verbose_name=_('Status'))
    seller = models.ForeignKey("user.Seller", on_delete=models.CASCADE, verbose_name=_('Seller'),
                               related_name="sectors", null=True, blank=True)

    class Meta:
        verbose_name = _("Sector")
        verbose_name_plural = _("Sectors")

    def __str__(self):
        return self.name


class SubLocation(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    status = models.BooleanField(default=False, verbose_name=_('Status'))
    location = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='sub_locations',
                                 verbose_name=_('Location'))
    seller = models.ForeignKey("user.Seller", on_delete=models.CASCADE, verbose_name=_('Seller'), null=True, blank=True)

    class Meta:
        verbose_name = _("Sub Location")
        verbose_name_plural = _("Sub Locations")

    def __str__(self):
        return self.name


class Location(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    status = models.BooleanField(default=False, verbose_name=_('Status'))
    latitude = models.FloatField(default=0, verbose_name=_('Latitude'))
    longitude = models.FloatField(default=0, verbose_name=_('Longitude'))
    seller = models.ForeignKey("user.Seller", on_delete=models.CASCADE, verbose_name=_('Seller'), null=True, blank=True)

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")

    def __str__(self):
        return self.name


class MedicalSector(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    status = models.BooleanField(default=False, verbose_name=_('Status'))
    inn_number = models.IntegerField(default=0, verbose_name=_('Inner Number'))
    seller = models.ForeignKey("user.Seller", on_delete=models.CASCADE, verbose_name=_('Seller'), null=True, blank=True)

    class Meta:
        verbose_name = _("Medical Sector")
        verbose_name_plural = _("Medical Sectors")

    def __str__(self):
        return self.name


phone_validator = RegexValidator(
    regex=r"^\+998\d{9}$", message=_("Phone number doesn't match"), code='invalid'
)


class CustomerStatus(models.TextChoices):
    ACTIVE = 'active', _('Active')
    IN_PROGRESS = 'in_progress', _('In Progress')
    IN_BASE = 'in_base', _('In Base')
    FROZEN = 'frozen', _('Frozen')
    ARCHIVED = 'archived', _('Archived')
    DELETED = 'deleted', _('Deleted')


class PaymentType(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    status = models.BooleanField(default=True, verbose_name=_('Status'))
    image = models.ImageField(upload_to='payment_type/', verbose_name=_('Image'), null=True, blank=True)

    def __str__(self):
        return self.name


class PaymentMethod(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    status = models.BooleanField(default=True, verbose_name=_('Status'))


class Customer(BaseModel):

    name = models.CharField(max_length=255, verbose_name=_('Name'), null=True, blank=True)
    copy_customer = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='copies',
                                      verbose_name=_('Copy Customer'))
    seller = models.ForeignKey('user.Seller', on_delete=models.CASCADE, related_name='customers',
                               verbose_name=_('Seller'))
    sector = models.ForeignKey('Sector', on_delete=models.CASCADE, related_name='customers', verbose_name=_('Sector'))
    location = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='customers',
                                 verbose_name=_('Location'))
    medical = models.ForeignKey('MedicalSector', on_delete=models.CASCADE, related_name='customers',
                                verbose_name=_('Medical Sector'))
    source = models.ForeignKey('Source', on_delete=models.CASCADE, related_name='customers', verbose_name=_('Source'))
    products = models.ManyToManyField('Product', related_name='customers', verbose_name=_('Products'))
    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE, related_name='customers', null=True, blank=True,)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, related_name='customers', null=True, blank=True,)
    status = models.CharField(max_length=20, choices=CustomerStatus.choices, default=CustomerStatus.IN_PROGRESS,
                              verbose_name=_('Status'))
    reactivate_data = models.DateTimeField(null=True, blank=True, verbose_name=_('Reactivate Data'))
    extra_phone = models.CharField(max_length=20, verbose_name=_('Extra Phone'), null=True, blank=True)
    telegram_phone = models.CharField(max_length=20, verbose_name=_('Telegram Phone'), null=True, blank=True, )
    phone_number = models.CharField(max_length=20, verbose_name=_('Phone Number'))
    recall_date = models.DateTimeField(null=True, blank=True, verbose_name=_('Recall Date'))
    status_changed_at = models.DateTimeField(null=True, verbose_name=_('Status Changed at'))

    def save(self, *args, **kwargs):
        if self.status == CustomerStatus.IN_BASE:
            other_customers = Customer.objects.filter(
                phone_number=self.phone_number,
                status=CustomerStatus.IN_BASE
            ).exclude(id=self.id)

            for customer in other_customers:
                customer.status = CustomerStatus.ARCHIVED
                customer.save()

        super().save(*args, **kwargs)

    @property
    def original_seller(self):
        first_customer = Customer.objects.filter(phone_number=self.phone_number).order_by('created_at').first()
        if first_customer:
            return {
                "id": first_customer.seller.id,
                "image_url": "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png",
                "name": first_customer.seller.full_name,
                "phone_number": first_customer.seller.phone
            }
        return None

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")

    def __str__(self):
        return self.name


class Source(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    status = models.BooleanField(default=False, verbose_name=_('Status'))
    seller = models.ForeignKey("user.Seller", on_delete=models.CASCADE, verbose_name=_('Seller'), null=True, blank=True)
    image = models.ImageField(upload_to='source/', verbose_name=_('Image'), null=True, blank=True)

    @property
    def image_url(self):
        path = 'https://static.thenounproject.com/png/5733136-200.png'
        return path if not self.image else self.image

    class Meta:
        verbose_name = _("Source")
        verbose_name_plural = _("Sources")

    def __str__(self):
        return self.name


class Product(BaseModel):
    image = models.ImageField(upload_to='products/', verbose_name=_('Image'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    seller = models.ForeignKey("user.Seller", on_delete=models.CASCADE, verbose_name=_('Seller'), null=True, blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.name


class StatusChangeRequest(BaseModel):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        ACCEPTED = 'accepted', 'Accepted'
        REJECTED = 'rejected', 'Rejected'
        ARCHIVED = 'archived', 'Archived'

    class Types(models.TextChoices):
        CUSTOMER = 'customer', 'Customer'
        COMMENT = 'comment', 'Comment'

    type = models.CharField(max_length=20, choices=Types.choices, default=Types.COMMENT,
                            verbose_name=_('Type'))
    comment = models.ForeignKey("user.Comment", on_delete=models.CASCADE, related_name='status_change_requests_comment',
                                verbose_name=_('Comment'), null=True,
                                blank=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='status_change_requests_customer',
                                 verbose_name=_('Customer'), null=True, blank=True)
    seller = models.ForeignKey('user.Seller', on_delete=models.CASCADE, related_name='status_change_requests_seller',
                               verbose_name=_('Seller'))
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING,
                              verbose_name=_('Status'))
    new_status = models.CharField(max_length=20, choices=CustomerStatus.choices, verbose_name=_('New Status'),
                                  null=True, blank=True, )
    comment_status = models.BooleanField(default=True)
    text = models.CharField(max_length=255, verbose_name=_('Text'))
    admin_response = models.CharField(max_length=255, verbose_name=_('Admin Response'))
    approved_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Approved At'))

    def approve(self):
        self.status = self.Status.ACCEPTED
        self.approved_at = datetime.datetime.now()
        self.save()

        self.customer.status = self.new_status
        self.customer.status_changed_at = timezone.now()
        self.customer.save()

        if self.new_status == CustomerStatus.ACTIVE:
            copied_customers = Customer.objects.filter(phone_number=self.customer.phone_number)
            for customer in copied_customers:
                customer.status = CustomerStatus.ARCHIVED
                customer.status_changed_at = datetime.datetime.now()
                customer.save()

    def reject(self, response_text=None):
        self.status = self.Status.REJECTED
        self.admin_response = response_text

    def __str__(self):
        return f"Request to change {self.customer.name}'s status to {self.new_status}"

    class Meta:
        verbose_name = _("Status Change Request")
        verbose_name_plural = _("Status Change Requests")


class RequestStatus(models.TextChoices):
    PENDING = 'pending', _('Pending')
    APPROVED = 'approved', _('Approved')
    REJECTED = 'rejected', _('Rejected')
