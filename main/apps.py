from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'
    verbose_name = 'Реестр'

    def ready(self):
        import main.signals
