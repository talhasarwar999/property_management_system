from django.urls import path
from . import views

urlpatterns = [

    # Tenant Dashboard urls
    path("tenant-dashboard/", views.tenant_dashboard, name="tenant-dashboard"),

    # Tenant Profile urls
    path("tenant-profile/", views.tenant_profile, name="tenant-profile"),
    path("change-tenant-password/", views.change_tenant_password, name="change-tenant-password"),

    # Tenant urls
    path("tenant-list/", views.tenant_list, name="tenant-list"),
    path("broker-tenant-list/", views.broker_tenant_list, name="broker-tenant-list"),
    path("delete-tenant/<pk>/", views.delete_tenant, name="delete-tenant"),
    path("view-tenant/<pk>/", views.view_tenant, name="view-tenant"),
    path("edit-tenant/<pk>/", views.edit_tenant, name="edit-tenant"),
    path("create-tenant/", views.create_tenant, name="create-tenant"),
]
