from django.contrib import admin
from .models import PropertyDealer, Property


class PropertyDealerAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'contact_number', 'address', 'email', 'website')

    def user(self, obj):
        return obj.user.username

    def email(self, obj):
        return obj.user.email

admin.site.register(PropertyDealer, PropertyDealerAdmin)
admin.site.register(Property)