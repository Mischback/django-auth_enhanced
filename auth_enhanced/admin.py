# -*- coding: utf-8 -*-
"""Contains app-specific admin classes."""

# Django imports
from django.contrib.admin import ModelAdmin, register

# app imports
from auth_enhanced.models import UserEnhancement


@register(UserEnhancement)
class UserEnhancementAdmin(ModelAdmin):
    """Integrates UserEnhancement into Django's admin menu.

    This ModelAdmin is just used for development and should not be registered
    in real production versions.
    UserEnhancements will be integrated into the respective admin class for
    the User-objects."""
    pass
