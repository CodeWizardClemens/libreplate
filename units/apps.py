from django.apps import AppConfig


class UnitsConfig(AppConfig):
    name = "units"

    def ready(self):
        import units.signals  # noqa
