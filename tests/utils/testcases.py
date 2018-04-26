# -*- coding: utf-8 -*-
"""Contains base classes for test cases"""

# Django imports
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.test import TestCase
from django.urls import resolve

# app imports
from auth_enhanced.email import callback_admin_information_new_signup
from auth_enhanced.models import UserEnhancement


class AuthEnhancedTestCase(TestCase):
    """Base class for all tests of django-auth_enhanced app."""
    pass


class AuthEnhancedNoSignalsTestCase(AuthEnhancedTestCase):
    """This test class disconnects all of the app's signal handlers."""

    @classmethod
    def setUpClass(cls):
        """Prepare the test environment by disconnecting signal handlers"""

        # call parent setUpClass
        super(AuthEnhancedNoSignalsTestCase, cls).setUpClass()

        # isolate the callback-method by disconnecting the signal handler
        post_save.disconnect(
            UserEnhancement.callback_create_enhancement_object,
            sender=get_user_model(),
            dispatch_uid='DAE_create_enhance_user_object'
        )

        post_save.disconnect(
            callback_admin_information_new_signup,
            sender=get_user_model(),
            dispatch_uid='DAE_admin_information_new_signup'
        )

    @classmethod
    def tearDownClass(cls):
        """Restore the test environment."""

        post_save.connect(
            UserEnhancement.callback_create_enhancement_object,
            sender=get_user_model(),
            dispatch_uid='DAE_create_enhance_user_object'
        )

        if settings.DAE_ADMIN_SIGNUP_NOTIFICATION:
            post_save.connect(
                callback_admin_information_new_signup,
                sender=get_user_model(),
                dispatch_uid='DAE_admin_information_new_signup'
            )

        # call the parent tearDownClass
        super(AuthEnhancedNoSignalsTestCase, cls).tearDownClass()


class AEUrlTestCase(AuthEnhancedNoSignalsTestCase):
    """Test cases for URL configuration

    Provides an additional assert()-method, 'assertCBVName' to check, if an url
    (specified by an url-string or an ResolverMatch-object) is connected with
    the right CBV."""

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
