from django.apps import AppConfig


class KchsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'KCHS'

    def ready(self):

        import KCHS.signals




