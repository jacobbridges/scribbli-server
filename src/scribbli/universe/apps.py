from django.apps import AppConfig


class UniverseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scribbli.universe'

    def ready(self):
        from scribbli.universe.signals.slugify import slugify_model
