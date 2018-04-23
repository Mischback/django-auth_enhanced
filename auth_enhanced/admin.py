# -*- coding: utf-8 -*-
"""Contains app-specific admin classes."""

# Django imports
from django.conf import settings
from django.contrib import admin

# app imports
from auth_enhanced.models import UserEnhancement


class UserEnhancementAdmin(admin.ModelAdmin):
    """Integrates UserEnhancement into Django's admin menu.

    This ModelAdmin is just used for development and should not be registered
    in real production versions.
    UserEnhancements will be integrated into the respective admin class for
    the User-objects."""
    pass


# register UserEnhancementAdmin only in DEBUG-mode
if settings.DEBUG:
    admin.site.register(UserEnhancement, UserEnhancementAdmin)
