from django.apps import AppConfig


class ApplicationConfig(AppConfig):
    name = 'application'
    verbose_name = 'l-ask'

    def ready(self):
        from application import signals
        super().ready()
