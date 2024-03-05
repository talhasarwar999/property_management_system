from django.urls import path
from . import views

urlpatterns = [

    # Broker Dashboard urls
    path("broker-dashboard/", views.broker_dashboard, name="broker-dashboard"),
    path("broker-profile/", views.broker_profile, name="broker-profile"),
    path("change-broker-password/", views.change_broker_password, name="change-broker-password"),

    # Broker urls
    path("broker-list/", views.broker_list, name="broker-list"),
    path("delete-broker/<pk>/", views.delete_broker, name="delete-broker"),
    path("view-broker/<pk>/", views.view_broker, name="view-broker"),
    path("create-broker/", views.create_broker, name="create-broker"),
    path("edit-broker/<pk>/", views.edit_broker, name="edit-broker"),
]
