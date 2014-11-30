from django.apps import AppConfig

class CuratrConfig(AppConfig):
    name = 'main'

    def ready(self):
        import main.signals
