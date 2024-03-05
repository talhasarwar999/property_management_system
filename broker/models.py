from django.db import models
from django.conf import settings

class BrokerFile(models.Model):
    file = models.FileField(upload_to='broker_documents/')
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=255, choices=[('profile', 'Profile'), ('document', 'Document'), ('image', 'Image')])

class Broker(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='broker_user')
    name = models.CharField(max_length=255, unique=True)
    contact_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255, blank=True, null=True)
    files = models.ManyToManyField(BrokerFile, related_name='broker_files')
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    license_number = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    years_of_experience = models.IntegerField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    is_accepting_new_clients = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name