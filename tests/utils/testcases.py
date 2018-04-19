# -*- coding: utf-8 -*-
"""Contains base classes for test cases"""

# Django imports
from django.test import TestCase
from django.urls import resolve


class AuthEnhancedTestCase(TestCase):
    """Base class for all tests of django-auth_enhanced app."""
    pass


class AEUrlTestCase(AuthEnhancedTestCase):
    """Test cases for URL configuration"""

    class InvalidParameterException(Exception):
        """Raised if one of the assert()-methods is called without correct parameters."""
        pass

    def assertCBVName(self, cbv_name, module='auth_enhanced.views', resolver_match=None, url=None):
        """Asserts the view function to be used to serve the URL."""

        # either a ResolverMatch object or an URL-string must be given
        if not resolver_match and not url:
            raise self.InvalidParameterException("You have to pass either 'resolver_match' or 'url'!")

        # get the ResolverMatch object by URL
        if not resolver_match:
            resolver_match = resolve(url)

        # test the name of the CBV (class name)
        self.assertEqual(resolver_match.func.__name__, cbv_name)

        # test the name of the containing module
        self.assertEqual(resolver_match.func.__module__, module)
