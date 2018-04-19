# -*- coding: utf-8 -*-
"""Contains base classes for test cases"""

# Django imports
from django.urls import resolve
from django.test import TestCase


class AuthEnhancedTestCase(TestCase):
    """Base class for all tests of django-auth_enhanced app."""
    pass


class AEUrlTestCase(AuthEnhancedTestCase):
    """Test cases for URL configuration"""

    class InvalidParameterException(Exception):
        """Raised if one of the assert()-methods is called without correct parameters."""
        pass

    def assertFuncName(self, func_name, resolver_match=None, url=None):
        """Asserts the view function to be used to serve the URL.

        Even if the parameter is called 'func_name', for CBVs the name of the
        class must be passed."""

        # either a ResolverMatch object or an URL-string must be given
        if not resolver_match and not url:
            raise self.InvalidParameterException("You have to pass either 'resolver_match' or 'url'!")

        # get the ResolverMatch object by URL
        if not resolver_match:
            resolver_match = resolve(url)

        self.assertEqual(resolver_match.func.__name__, func_name)
