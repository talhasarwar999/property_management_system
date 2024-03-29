from django.db import models
from django.conf import settings
from tanant.models import Tanant


class PropertyDealer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='property_dealer_logos/', blank=True, null=True)

    def __str__(self):
        return self.company_name


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.description or "Image"

class Document(models.Model):
    file = models.FileField(upload_to='documents/')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.description or "Document"



class Broker(models.Model):
    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Property(models.Model):
    PROPERTY_TYPES = [('rented', 'Rented'), ('sold', 'Sold'), ('free', 'Free'), ('off-plan', 'Off-Plan')]
    STATUS_CHOICES = [('available', 'Available'), ('not available', 'Not Available')]
    owner = models.ForeignKey(PropertyDealer, on_delete=models.CASCADE)
    broker = models.ForeignKey(Broker, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    address = models.TextField()
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    images = models.ManyToManyField(Image)
    documents = models.ManyToManyField(Document)
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

    def __str__(self):
        return self.title


class RentalAgreement(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tanant, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    agreement_document = models.OneToOneField(Document, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.property.title} - {self.tenant.name}"

class Lead(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    interested_party = models.CharField(max_length=255)
    meeting_time = models.DateTimeField()
    meeting_location = models.CharField(max_length=255)
    meeting_agenda = models.TextField()
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')])

    def __str__(self):
        return f"{self.interested_party} - {self.property.title}"

class Invoice(models.Model):
    rental_agreement = models.ForeignKey(RentalAgreement, on_delete=models.CASCADE)
    date_issued = models.DateTimeField()
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateTimeField()
    status = models.CharField(max_length=50, choices=[('unpaid', 'Unpaid'), ('paid', 'Paid')])
    invoice_pdf = models.OneToOneField(Document, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Invoice {self.id} for {self.rental_agreement.property.title}"