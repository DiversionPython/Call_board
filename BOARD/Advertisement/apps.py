from django.apps import AppConfig


class AdvertisementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Advertisement'

    # def ready(self):
    #     import Advertisement.signals
