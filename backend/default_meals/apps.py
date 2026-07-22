from django.apps import AppConfig


class DefaultMealsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "default_meals"

    def ready(self):
        pass
