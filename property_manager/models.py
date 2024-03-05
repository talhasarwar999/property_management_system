from django.db import models
from django.conf import settings
from tanant.models import Tanant
from broker.models import Broker


class PropertyDealer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='property_dealer_user')
    company_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='property_dealer_logos/', blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name



class PropertyFile(models.Model):
    file = models.FileField(upload_to='property_documents/')
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=255, choices=[('profile', 'Profile'), ('document', 'Document'), ('image', 'Image')])


class Property(models.Model):
    PROPERTY_TYPES = [('rented', 'Rented'), ('sold', 'Sold'), ('free', 'Free'), ('off-plan', 'Off-Plan')]
    STATUS_CHOICES = [('available', 'Available'), ('not available', 'Not Available')]
    owner = models.ForeignKey(PropertyDealer, on_delete=models.CASCADE)
    broker = models.ForeignKey(Broker, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    address = models.TextField()
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    files = models.ManyToManyField(PropertyFile)
    location = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    est_rent = models.FloatField(null=True, blank=True)
    total_area = models.FloatField(null=True, blank=True)
    num_rooms = models.IntegerField(null=True, blank=True)
    num_bathrooms = models.IntegerField(null=True, blank=True)
    est_delivery_time = models.DateTimeField(null=True, blank=True)
    construction_year = models.IntegerField(null=True, blank=True)
    has_swimming_pool = models.BooleanField(default=False)
    has_garden = models.BooleanField(default=False)
    has_garage = models.BooleanField(default=False)
    listing_details = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class RentalAgreement(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tanant, on_delete=models.CASCADE)
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE, blank=True, null=True)
    lease_start_date = models.DateTimeField()
    lease_end_date = models.DateTimeField()
    monthly_rent_tenant = models.FloatField(null=True, blank=True)
    broker_commission = models.FloatField(null=True, blank=True)
    security_deposit = models.FloatField(null=True, blank=True)
    late_payment_fee = models.FloatField(null=True, blank=True)
    maintenance_responsibilities = models.TextField(blank=True, null=True)
    renewal_terms = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.property.title} - {self.tenant.name}"

class Lead(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    interested_party = models.CharField(max_length=255)
    meeting_time = models.DateTimeField()
    meeting_location = models.CharField(max_length=255)
    meeting_agenda = models.TextField()
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')])
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.interested_party} - {self.property.title}"

class Invoice(models.Model):
    rental_agreement = models.ForeignKey(RentalAgreement, on_delete=models.CASCADE)
    date_issued = models.DateTimeField()
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateTimeField()
    status = models.CharField(max_length=50, choices=[('unpaid', 'Unpaid'), ('paid', 'Paid')])
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice {self.id} for {self.rental_agreement.property.title}"