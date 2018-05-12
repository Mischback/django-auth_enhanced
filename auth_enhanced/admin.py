# -*- coding: utf-8 -*-
"""Contains app-specific admin classes."""

# Django imports
from django.conf import settings
from django.contrib.admin import ModelAdmin, register, site
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

# app imports
from auth_enhanced.models import UserEnhancement


def register_only_debug(*models, **kwargs):
    """Register the given model(s) classes and wrapped ModelAdmin class with
    admin site, if DEBUG=True in project's settings.

    See https://github.com/django/django/blob/master/django/contrib/admin/decorators.py
    for the original Django implementation.

    TODO: Using '**kwargs' doesn't mimic Django2.0 codebase, but Django1.11!"""

    # need a callable here, but just 'pass'ing is fine...
    def _wrapper_noop(admin_class):
        pass

    if settings.DEBUG:
        # re-use Django's register-decorator
        return register(*models, **kwargs)

    # return a noop
    return _wrapper_noop


class EnhancedUserAdmin(UserAdmin):
    """This class substitutes the default admin interface for user objects.

    It is designed to enhance and substitute the default admin interface
    provided by 'django.contrib.auth'. But furthermore, it should be as
    pluggable as possible, to be able to deal with custom user models."""

    # 'list_display' controls, which fields will be displayed in the list view.
    # This is configurable with an app-specific setting or will be left at
    # Django's default value:
    #   ('username', 'email', 'first_name', 'last_name', 'is_staff')
    # TODO: Django already checks the value of 'list_display', so it might be
    #   unnecessary to actually check DAE_ADMIN_LIST_DISPLAY within the app.
    #   However, it should be ensured, that the app's setting only includes
    #   valid values, which depends on the AUTH_USER_MODEL in use.
    try:
        list_display = settings.DAE_ADMIN_LIST_DISPLAY
    except AttributeError:
        pass


@register_only_debug(UserEnhancement)
class UserEnhancementAdmin(ModelAdmin):
    """Integrates UserEnhancement into Django's admin menu.

    This ModelAdmin is just used for development and should not be registered
    in real production versions.
    UserEnhancements will be integrated into the respective admin class for
    the User-objects."""
    pass


# substitute the default implementation of the user admin
# TODO: should this be configurable?
site.unregister(get_user_model())
site.register(get_user_model(), EnhancedUserAdmin)
