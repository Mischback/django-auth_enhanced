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
from django.utils.translation import ugettext_lazy as _

# #############################################################################
# CONSTANTS
# #############################################################################

# This mode will automatically activate newly registered accounts
DAE_MODE_AUTO_ACTIVATION = 'DAE_MODE_AUTO_ACTIVATION'

# This mode sends a verification email and will automaticall activate the
#   newly registered account after successfull verification
DAE_MODE_EMAIL_ACTIVATION = 'DAE_MODE_EMAIL_ACTIVATION'

# This mode will *NOT* activate newly registered accounts and relies on manual
#   activation by a superuser
DAE_MODE_MANUAL_ACTIVATION = 'DAE_MODE_MANUAL_ACTIVATION'

# contains the app's operation modes to be used in a model (choices) field
# DAE_OPERATION_MODE_CHOICES = (
#     (DAE_MODE_AUTO_ACTIVATION, _('Automatic activation')),
#     (DAE_MODE_MANUAL_ACTIVATION, _('Manual activation')),
#     (DAE_MODE_EMAIL_ACTIVATION, _('EMail activation')),
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

    # ### DAE_OPERATION_MODE
    # This setting determines the way newly registered are handled.
    # Possible values:
    #   DAE_MODE_AUTO_ACTIVATION (default value)
    #       - newly created accounts will automatically get activated.
    #   DAE_MODE_EMAIL_ACTIVATION
    #       - newly created accounts will receive a verification mail. The
    #           account get activated automatically, when the email address
    #           is verified
    #   DAE_MODE_MANUAL_ACTIVATION
    #       - this mode will *NOT* activate newly registered accounts and
    #           relies on manual activation by a superuser
    inject_setting('DAE_OPERATION_MODE', DAE_MODE_AUTO_ACTIVATION)
