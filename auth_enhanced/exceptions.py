# -*- coding: utf-8 -*-
"""Contains app-specific exceptions."""


class AuthEnhancedException(Exception):
    """Base class for all app-specific exceptions."""
    pass


class AuthEnhancedConversionError(AuthEnhancedException):
    """This exception is raised by 'settings.convert_to_seconds()'."""
    pass
