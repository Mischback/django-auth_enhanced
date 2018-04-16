# -*- coding: utf-8 -*-
"""django-auth_enhanced: Application configuration

Provides the AppConfig class, that is required by Django. Within its 'ready()'
method, app-specific settings are injected (meaning: default values are
provided here, if they are not already given in the project's settings-module)
and app-specific checks are performed (using Django's check framework)."""

# Django imports
from django.apps import AppConfig


class AuthEnhancedConfig(AppConfig):
    """App specific configuration class"""

    name = 'auth_enhanced'
    verbose_name = 'auth_enhanced'

    def ready(self):
        """Executed, when application loading is completed."""
        pass
