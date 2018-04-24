# -*- coding: utf-8 -*-
"""Contains all app-specific settings with their respective default value.

Please note, that this file is more or less just a glossary of the settings,
that can be used in a project's settings module.
The 'injection' of these settings (meaning: providing their default value,
if not provided through a project's settings module) is done in this app's
'AppConfig'-class (see 'apps.py')."""


# Django imports
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _  # noqa

# #############################################################################
# CONSTANTS
# #############################################################################

# the default location for mail templates
#   In this app, this means 'auth_enhanced/templates/auth_enhanced/mail/'.
#   Please note: There is no trailing slash!
DAE_CONST_EMAIL_TEMPLATE_PREFIX = 'auth_enhanced/mail'

# This mode will automatically activate newly registered accounts
DAE_CONST_MODE_AUTO_ACTIVATION = 'DAE_CONST_MODE_AUTO_ACTIVATION'

# This mode sends a verification email and will automaticall activate the
#   newly registered account after successfull verification
DAE_CONST_MODE_EMAIL_ACTIVATION = 'DAE_CONST_MODE_EMAIL_ACTIVATION'

# This mode will *NOT* activate newly registered accounts and relies on manual
#   activation by a superuser
DAE_CONST_MODE_MANUAL_ACTIVATION = 'DAE_CONST_MODE_MANUAL_ACTIVATION'

# contains the app's operation modes to be used in a model (choices) field
# DAE_CONST_OPERATION_MODE_CHOICES = (
#     (DAE_CONST_MODE_AUTO_ACTIVATION, _('Automatic activation')),
#     (DAE_CONST_MODE_MANUAL_ACTIVATION, _('Manual activation')),
#     (DAE_CONST_MODE_EMAIL_ACTIVATION, _('EMail activation')),
# )


# #############################################################################
# FUNCTIONS
# #############################################################################

def inject_setting(name, default_value):
    """Injects an app-specific setting into Django's settings module.

    If the setting is already present in the project's settings module, the set
    value will be used. If it is not present, it will be injected.

    The function will validate, that only uppercase setting-names will be used
    or raise an appropriate exception."""

    # check, that the name is uppercased
    if not name.isupper():
        raise ImproperlyConfigured('Only uppercase names are allowed!')

    # set the setting, if it is not already present
    if not hasattr(settings, name):
        setattr(settings, name, default_value)


def set_app_default_settings():
    """Sets all app-specific default settings."""

    # ### DAE_EMAIL_TEMPLATE_PREFIX
    # This setting determines the place to look for mail templates.
    # Please note, that the path must be reachable by Django's template engine.
    # Furthermore, it *must not* include a trailing slash.
    inject_setting('DAE_EMAIL_TEMPLATE_PREFIX', DAE_CONST_EMAIL_TEMPLATE_PREFIX)

    # ### DAE_OPERATION_MODE
    # This setting determines the way newly registered are handled.
    # Possible values:
    #   DAE_CONST_MODE_AUTO_ACTIVATION (default value)
    #       - newly created accounts will automatically get activated.
    #   DAE_CONST_MODE_EMAIL_ACTIVATION
    #       - newly created accounts will receive a verification mail. The
    #           account get activated automatically, when the email address
    #           is verified
    #   DAE_CONST_MODE_MANUAL_ACTIVATION
    #       - this mode will *NOT* activate newly registered accounts and
    #           relies on manual activation by a superuser
    inject_setting('DAE_OPERATION_MODE', DAE_CONST_MODE_AUTO_ACTIVATION)
