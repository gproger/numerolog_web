from django.apps import AppConfig


class EventsConfig(AppConfig):
    name = 'events'

    def ready(self):
        print("at ready")
        import events.signals
