from django.db import models
from django.conf import settings


# Create your models here.
class Tanant(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    property = models.ForeignKey('property_manager.property', on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    images = models.ManyToManyField('property_manager.Image')
    agreement_document = models.OneToOneField('property_manager.Document', on_delete=models.CASCADE, blank=True, null=True)
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
    logo = models.ImageField(upload_to='tenant_logos/', blank=True, null=True)

    def __str__(self):
        return self.name