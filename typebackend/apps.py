from django.apps import AppConfig


class TypebackendConfig(AppConfig):
    name = 'typebackend'

    def ready(self):
        import typebackend.signals