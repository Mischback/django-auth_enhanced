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
    DAE_CONST_MODE_MANUAL_ACTIVATION, DAE_CONST_RECOMMENDED_LOGIN_URL
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
        "purpose, you can safely ignore this setting.".format(DAE_CONST_RECOMMENDED_LOGIN_URL)
    ),
    id='dae.w001'
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

    # and now hope, this is still empty! ;)
    return errors
