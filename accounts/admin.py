from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_property_dealer', 'is_active', 'is_superuser', 'is_tenant')

admin.site.register(User, UserAdmin)