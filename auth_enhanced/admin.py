# -*- coding: utf-8 -*-
"""Contains app-specific admin classes."""

# Django imports
from django.conf import settings
from django.contrib.admin import ModelAdmin, register

# app imports
from auth_enhanced.models import UserEnhancement


def register_only_debug(*models, site=None):
    """Register the given model(s) classes and wrapped ModelAdmin class with
    admin site, if DEBUG=True in project's settings.

    See https://github.com/django/django/blob/master/django/contrib/admin/decorators.py
    for the original Django implementation."""

    # need a callable here, but just 'pass'ing is fine...
    def _wrapper_noop(admin_class):
        pass

    if settings.DEBUG:
        # re-use Django's register-decorator
        return register(*models, site=site)

    # return a noop
    return _wrapper_noop


@register_only_debug(UserEnhancement)
class UserEnhancementAdmin(ModelAdmin):
    """Integrates UserEnhancement into Django's admin menu.

    This ModelAdmin is just used for development and should not be registered
    in real production versions.
    UserEnhancements will be integrated into the respective admin class for
    the User-objects."""
    pass
