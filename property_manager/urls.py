from django.urls import path
from . import views

urlpatterns = [
    # Property Manager Dashboard urls
    path('property-manager-dashboard/', views.property_manager_dashboard, name='property-manager-dashboard'),

    # Property Manager Profile urls
    path('property-manager-profile/', views.property_manager_profile, name='property-manager-profile'),
    path("change-password/", views.change_password, name="change-password"),

    # Property urls
    path("property-list/", views.property_list, name="property-list"),
    path("delete-property/<pk>/", views.delete_property, name="delete-property"),
    path("view-property/<pk>/", views.view_property, name="view-property"),
    path("create-property/", views.create_property, name="create-property"),
    path("edit-property/<pk>/", views.edit_property, name="edit-property"),

    # Tenant urls
    path("tenant-list/", views.tenant_list, name="tenant-list"),
    path("delete-tenant/<pk>/", views.delete_tenant, name="delete-tenant"),
    path("view-tenant/<pk>/", views.view_tenant, name="view-tenant"),
    path("edit-tenant/<pk>/", views.edit_tenant, name="edit-tenant"),
    path("create-tenant/", views.create_tenant, name="create-tenant"),
]
