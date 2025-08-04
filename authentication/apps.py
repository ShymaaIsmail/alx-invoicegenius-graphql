from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    """Configuration for the Authentication application.
    This application handles user authentication, registration, and related functionalities."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'
