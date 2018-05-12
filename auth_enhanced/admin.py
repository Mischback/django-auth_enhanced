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
    pass


@register_only_debug(UserEnhancement)
class UserEnhancementAdmin(ModelAdmin):
    """Integrates UserEnhancement into Django's admin menu.

    This ModelAdmin is just used for development and should not be registered
    in real production versions.
    UserEnhancements will be integrated into the respective admin class for
    the User-objects."""
    pass


#
site.unregister(get_user_model())
site.register(get_user_model(), EnhancedUserAdmin)
