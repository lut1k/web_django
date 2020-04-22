from django.apps import AppConfig


class ApplicationConfig(AppConfig):
    name = 'application'

    def ready(self):
        from application import signals
        super().ready()
