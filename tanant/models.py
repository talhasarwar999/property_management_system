from django.db import models
from django.conf import settings
# from broker.models import Broker


class TanantFile(models.Model):
    file = models.FileField(upload_to='tanant_documents/')
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=255, choices=[('profile', 'Profile'), ('document', 'Document'), ('image', 'Image')])

# Create your models here.
class Tanant(models.Model):
    STATUS_CHOICES = [
        ('ON_RENT', 'On Rent'),
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tenant_user')
    property = models.ForeignKey('property_manager.property', on_delete=models.SET_NULL, blank=True, null=True)
    broker = models.ForeignKey('broker.broker', on_delete=models.SET_NULL, null=True, blank=True, related_name='broker_tenant_user')
    name = models.CharField(max_length=255, unique=True)
    contact_number = models.CharField(max_length=15)
    files = models.ManyToManyField(TanantFile, related_name='tenant_files')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING', blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    lease_start_date = models.DateField()
    lease_end_date = models.DateField()
    rent_amount = models.FloatField()
    security_deposit = models.FloatField()
    payment_history = models.TextField(blank=True, null=True)
    annual_income = models.FloatField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name