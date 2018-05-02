# -*- coding: utf-8 -*-
"""Provides the AppConfig class, that is required by Django."""

# Django imports
from django.apps import AppConfig
from django.conf import settings
from django.core.checks import register
from django.db.models.signals import post_save
from django.utils import six

# app imports
from auth_enhanced.checks import check_settings_values
from auth_enhanced.email import (
    callback_admin_information_new_signup,
    callback_user_signup_email_verification,
)
from auth_enhanced.exceptions import AuthEnhancedConversionError
from auth_enhanced.settings import (
    DAE_CONST_MODE_EMAIL_ACTIVATION, DAE_CONST_VERIFICATION_TOKEN_MAX_AGE, convert_to_seconds, set_app_default_settings,
)


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

        # convert time-strings to seconds
        if isinstance(settings.DAE_VERIFICATION_TOKEN_MAX_AGE, six.string_types):
            try:
                setattr(
                    settings,
                    'DAE_VERIFICATION_TOKEN_MAX_AGE',
                    convert_to_seconds(settings.DAE_VERIFICATION_TOKEN_MAX_AGE)
                )
            except AuthEnhancedConversionError:
                setattr(
                    settings,
                    'DAE_VERIFICATION_TOKEN_MAX_AGE',
                    DAE_CONST_VERIFICATION_TOKEN_MAX_AGE
                )

        # register app-specific system checks
        register(check_settings_values)

        # add a 'post_save'-callback to automatically create a UserEnhancement,
        #   whenever a User-object is created.
        post_save.connect(
            self.get_model('UserEnhancement').callback_create_enhancement_object,
            sender=settings.AUTH_USER_MODEL,
            dispatch_uid='DAE_create_enhance_user_object'
        )

        # add a 'post_save'-callback to inform admins/superusers about a newly
        #   registered user.
        #   Please note: the callback is only registered, if the corresponding
        #   setting is not False.
        if settings.DAE_ADMIN_SIGNUP_NOTIFICATION:
            post_save.connect(
                callback_admin_information_new_signup,
                sender=settings.AUTH_USER_MODEL,
                dispatch_uid='DAE_admin_information_new_signup'
            )

        # add a 'post_save'-callback to send an email to the newly registered
        #   user, if 'DAE_OPERATION_MODE' == 'DAE_CONST_MODE_EMAIL_ACTIVATION'.
        #   This means, an automatic email verification is only available in
        #   that mode. However, users may verify their email addresses by a
        #   manual process.
        if settings.DAE_OPERATION_MODE == DAE_CONST_MODE_EMAIL_ACTIVATION:
            post_save.connect(
                callback_user_signup_email_verification,
                sender=settings.AUTH_USER_MODEL,
                dispatch_uid='DAE_user_signup_email_verification'
            )
