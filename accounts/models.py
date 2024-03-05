from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_property_dealer = models.BooleanField(default=False)
    is_tenant = models.BooleanField(default=False)
    is_broker = models.BooleanField(default=False)