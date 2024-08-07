from django.apps import AppConfig


class MainAuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Main_Auth"

    def ready(self):
        import Main_Auth.signals  # Import the signals to ensure they are registered
