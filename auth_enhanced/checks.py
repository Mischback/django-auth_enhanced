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
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils import six
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

# DAE_ADMIN_SIGNUP_NOTIFICATION
E003 = Error(
    _("'DAE_ADMIN_SIGNUP_NOTIFICATION' is set to an invalid value!"),
    hint=_(
        "Please check your settings and ensure, that 'DAE_ADMIN_SIGNUP_NOTIFICATION' "
        "is either set to boolean 'False' or a list of tuples, following the "
        "form of '(USERNAME, EMAIL_ADDRESS, (NOTIFICATION_METHOD, )),', where "
        "USERNAME is a valid username, EMAIL_ADDRESS the corresponding and "
        "verified email address and a tuple of supported NOTIFICATION_METHODs. "
        "Currently supported method is 'mail'."
    ),
    id='dae.e003'
)

# DAE_EMAIL_ADMIN_NOTIFICATION_PREFIX
E004 = Error(
    _("'DAE_EMAIL_ADMIN_NOTIFICATION_PREFIX' has to be a string!"),
    hint=_(
        "Please check your settings and ensure, that 'DAE_EMAIL_ADMIN_NOTIFICATION_PREFIX' "
        "is set to a string-value (default: '')."
    ),
    id='dae.e004'
)

# LOGIN_URL (Django settings)
W005 = Warning(
    _("'LOGIN_URL' does not point to the login url provided by 'django-auth_enhanced'."),
    hint=_(
        "The suggested value for 'LOGIN_URL' is '{}', which "
        "provides the built-in login view. If you set another login url on "
        "purpose, you can safely ignore this warning.".format(DAE_CONST_RECOMMENDED_LOGIN_URL)
    ),
    id='dae.w005'
)

# mail settings
W006 = Warning(
    _("Your email settings are identical to Django's default values!"),
    hint=_(
        "While it may absolutely be possible to run your Django project with "
        "these settings, it seems unlikely. If you keep receiving exceptions "
        "while running 'django-auth_enhanced', please check your settings. "
        "If everything works just fine, you can safely ignore this warning."
    ),
    id='dae.w006'
)

# DAE_EMAIL_FROM_ADDRESS
W007 = Warning(
    _("'DAE_EMAIL_FROM_ADDRESS' is not set to a valid email address!"),
    hint=_(
        "It is highly recommended to set 'DAE_EMAIL_FROM_ADDRESS' to a valid "
        "email address. Without a valid email address in the 'to'-header, your "
        "project's mails will probably end up in a spam folder (this does not "
        "mean, that they will *not* end in a spam folder, if you provide a "
        "valid address here)."
    ),
    id='dae.w007'
)

# DAE_EMAIL_PREFIX
E008 = Error(
    _("'DAE_EMAIL_PREFIX' has to be a string!"),
    hint=_(
        "Please check your settings and ensure, that 'DAE_EMAIL_PREFIX' is set "
        "to a string-value (default: '')."
    ),
    id='dae.e008'
)

# DAE_SALT
E009 = Error(
    _("'DAE_SALT' has to be a string!"),
    hint=_(
        "Please check your settings and ensure, that 'DAE_SALT' is set to a "
        "string-value (default: 'django-auth_enhanced')."
    ),
    id='dae.e009'
)

# DAE_VERIFICATION_TOKEN_MAX_AGE
E010 = Error(
    _("'DAE_VERIFICATION_TOKEN_MAX_AGE' has to be an integer!"),
    hint=_(
        "Please check your settings and ensure, that "
        "'DAE_VERIFICATION_TOKEN_MAX_AGE' is set to an integer value or a "
        "string with either a trailing 'h' or 'd' and leading numbers."
    ),
    id='dae.e010'
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

    # DAE_ADMIN_SIGNUP_NOTIFICATION
    #   This needs a little more effort, because the structure and the values
    #   inside of the structure need attention.
    #   The 'e03' controls, if the error has to be raised; this is not like the
    #   most elegant way, but it works...
    e03 = False
    if (isinstance(settings.DAE_ADMIN_SIGNUP_NOTIFICATION, bool)):
        if settings.DAE_ADMIN_SIGNUP_NOTIFICATION is True:
            e03 = True
    else:
        for tup in settings.DAE_ADMIN_SIGNUP_NOTIFICATION:
            try:
                validate_email(tup[1])
            except (IndexError, ValidationError):
                e03 = True
                break
            for method in tup[2]:
                # this is the place to list available methods of notification
                if method not in ('mail'):
                    e03 = True
                    break
    # append 'E003' if any error was found
    if e03:
        errors.append(E003)

    # DAE_EMAIL_ADMIN_NOTIFICATION_PREFIX
    if not isinstance(settings.DAE_EMAIL_ADMIN_NOTIFICATION_PREFIX, six.string_types):
        errors.append(E004)

    # LOGIN_URL (Django settings)
    if settings.LOGIN_URL != DAE_CONST_RECOMMENDED_LOGIN_URL:
        errors.append(W005)

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
        errors.append(W006)

    # DAE_EMAIL_FROM_ADDRESS
    try:
        validate_email(settings.DAE_EMAIL_FROM_ADDRESS)
    except (IndexError, ValidationError):
        errors.append(W007)

    # DAE_EMAIL_PREFIX
    if not isinstance(settings.DAE_EMAIL_PREFIX, six.string_types):
        errors.append(E008)

    # DAE_SALT
    if not isinstance(settings.DAE_SALT, six.string_types):
        errors.append(E009)

    # DAE_VERIFICATION_TOKEN_MAX_AGE
    if not isinstance(settings.DAE_VERIFICATION_TOKEN_MAX_AGE, six.integer_types):
        errors.append(E010)

    # and now hope, this is still empty! ;)
    return errors
