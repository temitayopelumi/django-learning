from django.apps import AppConfig


class CheckConfig(AppConfig):
    name = 'check'

    def ready(self):
        import check.signals
