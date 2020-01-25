from django.apps import AppConfig


class SchoolformConfig(AppConfig):
    name = 'schoolform'

    def ready(self):
        import schoolform.signals
