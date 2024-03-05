from django.apps import AppConfig


class TanantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tanant'

    # def ready(self):
    #     import tanant.signals
