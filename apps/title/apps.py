from django.apps import AppConfig


class TitleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.title'

    def ready(self):
        import apps.title.signals
