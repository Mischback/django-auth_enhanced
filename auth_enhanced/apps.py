# -*- coding: utf-8 -*-
"""Provides the AppConfig class, that is required by Django."""

# Django imports
from django.apps import AppConfig
from django.core.checks import register

# app imports
from auth_enhanced.checks import check_settings_values
from auth_enhanced.settings import set_app_default_settings


class AuthEnhancedConfig(AppConfig):
    """App specific configuration class

    Within its 'ready()'-method, app-specific settings are injected (meaning:
    default values are provided here, if they are not already given in the
    project's settings-module) and app-specific checks are performed (using
    Django's check framework)."""

    name = 'auth_enhanced'
    verbose_name = 'auth_enhanced'

    def ready(self):
        """Executed, when application loading is completed."""

        # apply the default settings
        set_app_default_settings()

        # register app-specific system checks
        register(check_settings_values)
