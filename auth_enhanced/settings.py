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

# the name of the login url, as specified in 'urls.py'
DAE_CONST_RECOMMENDED_LOGIN_URL = 'auth_enhanced:login'


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

    # ### DAE_ADMIN_SIGNUP_NOTIFICATION
    # This setting controls, if emails will be sent to specified superusers/
    #   admins whenever a new user signs up.
    # Possible values:
    #   False
    #       - no emails will be sent (default value)
    #   List of tuples of the following form
    #       - (USERNAME, EMAIL_ADDRESS, (NOTIFICATION_METHOD, )),
    #       - ('django', 'django@localhost', ('mail', )),
    #           USERNAME must be a valid username of this Django project
    #           EMAIL_ADDRESS must be the verified email address of that user
    #           (NOTIFICATION_METHOD, ) must be a tuple containing supported
    #               notification methods. As of now, only 'mail' is supported
    inject_setting('DAE_ADMIN_SIGNUP_NOTIFICATION', False)

    # ### DAE_EMAIL_LINK_SCHEME
    # If mails sent by django-auth_enhanced contain links to the project
    #   website, use this 'scheme'.
    # 'scheme' is to be understood as specified in RFC3986
    #   https://tools.ietf.org/html/rfc3986#section-3
    # Possible values:
    #   - 'http'
    #   - 'https'
    # (injected outside alphabetical order because it gets referenced later!)
    inject_setting('DAE_EMAIL_LINK_SCHEME', 'http')

    # ### DAE_EMAIL_LINK_AUTHORITY
    # If mails send by django-auth_enhanced contain links to the project
    #   website, use this 'authority'.
    # 'authority' is to be understood as specified in RFC3986
    #   https://tools.ietf.org/html/rfc3986#section-3
    # (injected outside alphabetical order because it gets referenced later!)
    inject_setting('DAE_EMAIL_LINK_AUTHORITY', '127.0.0.1:8000')

    # ### DAE_EMAIL_ADMIN_NOTIFICATION_PREFIX
    # Mails sent by django-auth_enhanced will contain a subject with this
    #   customizable prefix.
    inject_setting('DAE_EMAIL_ADMIN_NOTIFICATION_PREFIX', '')

    # ### DAE_EMAIL_ADMIN_LINK_SCHEME
    # If mails sent by django-auth_enhanced addressed to superusers contain
    #   links to the project website, use this 'scheme'.
    # 'scheme' is to be understood as specified in RFC3986
    #   https://tools.ietf.org/html/rfc3986#section-3
    # Possible values:
    #   - 'http'
    #   - 'https'
    # Relies on DAE_EMAIL_LINK_SCHEME. If your admin site is served from the
    #   same Django instance, you shouldn't need to touch this setting.
    inject_setting('DAE_EMAIL_ADMIN_LINK_SCHEME', settings.DAE_EMAIL_LINK_SCHEME)

    # ### DAE_EMAIL_ADMIN_LNK_AUTHORITY
    # If mails send by django-auth_enhanced addressed to superusers contain
    #   links to the project website, use this 'authority'.
    # 'authority' is to be understood as specified in RFC3986
    #   https://tools.ietf.org/html/rfc3986#section-3
    # Relies on DAE_EMAIL_LINK_AUTHORITY. If your admin site is served from the
    #   same Django instance, you shouldn't need to touch this setting.
    inject_setting('DAE_EMAIL_ADMIN_LNK_AUTHORITY', settings.DAE_EMAIL_LINK_AUTHORITY)

    # ### DAE_EMAIL_FROM_ADDRESS
    # Mails sent by django-auth_enhanced will have the following 'from'-address.
    #   The default value relies on Django's DEFAULT_FROM_EMAIL-setting, which
    #   defaults to 'webmaster@localhost' itsself.
    #   You may choose to change the built-in Django-setting or this app's one.
    inject_setting('DAE_EMAIL_FROM_ADDRESS', settings.DEFAULT_FROM_EMAIL)

    # ### DAE_EMAIL_HOME_VIEW_NAME
    # The name of the home view (like in: the starting page of your project)
    inject_setting('DAE_EMAIL_HOME_VIEW_NAME', 'home')

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

    # ### DAE_PROJECT_NAME
    # This setting is used in emails as a project-specific branding.
    # Possible values: has to be a 'string'
    inject_setting('DAE_PROJECT_NAME', 'auth_enhanced - development')
