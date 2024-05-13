from django.apps import AppConfig


class VmsApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vms_api'

    def ready(self):
        import vms_api.signals
