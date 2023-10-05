from django.apps import AppConfig


class TradehookConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tradehook'

    def ready(self):
        import tradehook.signals