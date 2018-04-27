# -*- coding: utf-8 -*-
"""Contains base classes for test cases"""

# Django imports
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.test import TestCase
from django.urls import resolve

# app imports
from auth_enhanced.email import (
    callback_admin_information_new_signup,
    callback_user_signup_email_verification,
)
from auth_enhanced.models import UserEnhancement
from auth_enhanced.settings import DAE_CONST_MODE_EMAIL_ACTIVATION


class AuthEnhancedTestCaseBase(TestCase):
    """Base class for all tests of django-auth_enhanced app."""

    @classmethod
    def _disconnect_signal_callbacks(cls):
        """Disconnects all app-specific signal callbacks.

        This method is closely connected with
        'auth_enhanced.apps.AuthEnhancedConfig.ready()'. For convenience, all
        signals should be connected there. All connects have to be reverted
        here.

        Please note, that derived classes may use this classmethod in a
        'setUp'-method or 'setUpClass'-classmethod, depending on the actual
        requirement of the test cases."""

        # no need to 'try/except' anything here, 'disconnect()' fails gracefully
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

        post_save.disconnect(
            callback_user_signup_email_verification,
            sender=get_user_model(),
            dispatch_uid='DAE_user_signup_email_verification'
        )

    @classmethod
    def _reconnect_signal_callbacks(cls):
        """(Re-) connects all app-specific signal callbacks.

        This method is closely connected with
        'auth_enhanced.apps.AuthEnhancedConfig.ready()'. For convenience, all
        signals should be connected there. All connects have to be mimiced
        here, including logical constraints (i.e. dependency on some setting).

        Please note, that derived classes may use this classmethod in a
        'tearDown'-method or 'tearDownClass'-classmethod, depending on the
        actual requirement of the test cases."""

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

        if settings.DAE_OPERATION_MODE == DAE_CONST_MODE_EMAIL_ACTIVATION:
            post_save.connect(
                callback_user_signup_email_verification,
                sender=settings.AUTH_USER_MODEL,
                dispatch_uid='DAE_user_signup_email_verification'
            )


class AuthEnhancedTestCase(AuthEnhancedTestCaseBase):
    """This test class enables running tests without the app-specific
    signal handlers applied.

    The 'disconnect()' will be performed per test class to enhance performance
    and signal callbacks are 'reconnected' after all test-methods have been
    run."""

    @classmethod
    def setUpClass(cls):
        """Prepare the test environment."""

        # call parent setUpClass
        super(AuthEnhancedTestCase, cls).setUpClass()

        # disconnect app-specific signal callbacks
        cls._disconnect_signal_callbacks()

    @classmethod
    def tearDownClass(cls):
        """Restore the test environment."""

        # reconnect app-specific signal callbacks
        cls._reconnect_signal_callbacks()

        # call the parent tearDownClass
        super(AuthEnhancedTestCase, cls).tearDownClass()


class AuthEnhancedPerTestDeactivatedSignalsTestCase(AuthEnhancedTestCaseBase):
    """This test class enables running tests without the app-specific
    signal handlers applied on a 'per test-method' base.

    This is useful to actually test the connect-process."""

    def setUp(self):
        self._disconnect_signal_callbacks()

    def tearDown(self):
        self._reconnect_signal_callbacks()


class AEUrlTestCase(AuthEnhancedTestCase):
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
