# -*- coding: utf-8 -*-
"""Contains checks for app-specific details of the project's settings.

These checks are applied by Django's system check framework, see
https://docs.djangoproject.com/en/dev/ref/checks/ for details.

There are two different types of checks:
1) checks, that all app-specific settings are set to accepted values
2) checks, that the logical connection between different settings is valid"""


# Django imports
from django.conf import settings
from django.core.checks import Error, Warning
from django.utils.translation import ugettext_lazy as _

# app imports
from auth_enhanced.settings import (
    DAE_CONST_MODE_AUTO_ACTIVATION, DAE_CONST_MODE_EMAIL_ACTIVATION,
    DAE_CONST_MODE_MANUAL_ACTIVATION, DAE_CONST_RECOMMENDED_LOGIN_URL,
)

# DAE_OPERATION_MODE
E001 = Error(
    _("'DAE_OPERATION_MODE' is set to an invalid value!"),
    hint=_(
        "Please check your settings and ensure, that 'DAE_OPERATION_MODE' is "
        "set to one of the following values: '{}', '{}' or '{}'.".format(
            DAE_CONST_MODE_AUTO_ACTIVATION, DAE_CONST_MODE_EMAIL_ACTIVATION, DAE_CONST_MODE_MANUAL_ACTIVATION
        )
    ),
    id='dae.e001'
)

# DAE_EMAIL_TEMPLATE_PREFIX
E002 = Error(
    _("'DAE_EMAIL_TEMPLATE_PREFIX' must not have a trailing slash!"),
    hint=_(
        "Please check your settings and ensure, that 'DAE_EMAIL_TEMPLATE_PREFIX' "
        "does not end with a slash ('/')."
    ),
    id='dae.e002'
)

# LOGIN_URL (Django settings)
W001 = Warning(
    _("'LOGIN_URL' does not point to the login url provided by 'django-auth_enhanced'."),
    hint=_(
        "The suggested value for 'LOGIN_URL' is '{}', which "
        "provides the built-in login view. If you set another login url on "
        "purpose, you can safely ignore this warning.".format(DAE_CONST_RECOMMENDED_LOGIN_URL)
    ),
    id='dae.w001'
)

# mail settings
W002 = Warning(
    _("Your email settings are identical to Django's default values!"),
    hint=_(
        "While it may absolutely be possible to run your Django project with "
        "these settings, it seems unlikely. If you keep receiving exceptions "
        "while running 'django-auth_enhanced', please check your settings. "
        "If everything works just fine, you can safely ignore this warning."
    ),
    id='dae.w002'
)


def check_settings_values(app_configs, **kwargs):
    """Checks, if the app-specific settings have valid values."""

    errors = []

    # DAE_OPERATION_MODE
    if settings.DAE_OPERATION_MODE not in (
        DAE_CONST_MODE_AUTO_ACTIVATION, DAE_CONST_MODE_EMAIL_ACTIVATION, DAE_CONST_MODE_MANUAL_ACTIVATION
    ):
        errors.append(E001)

    # DAE_EMAIL_TEMPLATE_PREFIX
    if settings.DAE_EMAIL_TEMPLATE_PREFIX[-1:] == '/':
        errors.append(E002)

    # LOGIN_URL (Django settings)
    if settings.LOGIN_URL != DAE_CONST_RECOMMENDED_LOGIN_URL:
        errors.append(W001)

    # mail settings
    #   This check is somehow fuzzy. Basically it checks, if all email-related
    #   settings are still at their provided default values. This *may*
    #   indicate, that the settings do not work.
    if (
        (settings.EMAIL_HOST == 'localhost') and
        (settings.EMAIL_PORT == 25) and
        (settings.EMAIL_HOST_USER == '') and
        (settings.EMAIL_HOST_PASSWORD == '') and
        (settings.EMAIL_USE_TLS is False) and
        (settings.EMAIL_USE_SSL is False) and
        (settings.EMAIL_TIMEOUT is None) and
        (settings.EMAIL_SSL_KEYFILE is None) and
        (settings.EMAIL_SSL_CERTFILE is None) and
        (settings.EMAIL_BACKEND == 'django.core.mail.backends.smtp.EmailBackend')
    ):
        errors.append(W002)

    # and now hope, this is still empty! ;)
    return errors
