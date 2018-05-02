# -*- coding: utf-8 -*-
"""Includes tests targeting the AppConfig class.

    - target file: auth_enhanced/admin.py
    - included tags: 'appconfig'"""

# Python imports
from unittest import skip  # noqa

# Django imports
from django.apps import apps
from django.db.models import signals
from django.test import override_settings, tag  # noqa

# app imports
from auth_enhanced.settings import (
    DAE_CONST_MODE_EMAIL_ACTIVATION, DAE_CONST_MODE_MANUAL_ACTIVATION,
)

# app imports
from .utils.testcases import AuthEnhancedPerTestDeactivatedSignalsTestCase


@tag('appconfig')
class AuthEnhancedConfigTests(AuthEnhancedPerTestDeactivatedSignalsTestCase):
    """These tests target the AppConfig."""

    @override_settings(
        DAE_ADMIN_SIGNUP_NOTIFICATION=False,
        DAE_OPERATION_MODE=DAE_CONST_MODE_MANUAL_ACTIVATION
    )
    def test_default_signals_registered(self):
        """Only 'DAE_create_enhance_user_object' is registered.

        See 'ready()'-method.

        'AuthEnhancedNoSignalsTestCase' is used as parent class for these
        tests. By calling 'ready()' again explicitly, the signals should be
        registered."""

        self.assertEqual(signals.post_save.receivers, [])

        # call this app's 'ready()'-method to register signal handlers
        apps.get_app_config('auth_enhanced').ready()

        dispatch_uids = [x[0][0] for x in signals.post_save.receivers]
        self.assertIn('DAE_create_enhance_user_object', dispatch_uids)
        self.assertNotIn('DAE_admin_information_new_signup', dispatch_uids)
        self.assertNotIn('DAE_user_signup_email_verification', dispatch_uids)

    @override_settings(DAE_ADMIN_SIGNUP_NOTIFICATION=(('foo', 'foo@localhost', ('mail', )), ),)
    def test_admin_signup_notification_registered(self):
        """'DAE_admin_information_new_signup' is registered.

        See 'ready()'-method.

        'AuthEnhancedNoSignalsTestCase' is used as parent class for these
        tests. By calling 'ready()' again explicitly, the signals should be
        registered."""

        self.assertEqual(signals.post_save.receivers, [])

        # call this app's 'ready()'-method to register signal handlers
        apps.get_app_config('auth_enhanced').ready()

        dispatch_uids = [x[0][0] for x in signals.post_save.receivers]
        self.assertIn('DAE_create_enhance_user_object', dispatch_uids)
        self.assertIn('DAE_admin_information_new_signup', dispatch_uids)

    @override_settings(DAE_OPERATION_MODE=DAE_CONST_MODE_EMAIL_ACTIVATION)
    def test_user_signup_email_verification_registered(self):
        """'DAE_user_signup_email_verification' is registered.

        See 'ready()'-method.

        'AuthEnhancedNoSignalsTestCase' is used as parent class for these
        tests. By calling 'ready()' again explicitly, the signals should be
        registered."""

        self.assertEqual(signals.post_save.receivers, [])

        # call this app's 'ready()'-method to register signal handlers
        apps.get_app_config('auth_enhanced').ready()

        dispatch_uids = [x[0][0] for x in signals.post_save.receivers]
        self.assertIn('DAE_create_enhance_user_object', dispatch_uids)
        self.assertIn('DAE_user_signup_email_verification', dispatch_uids)
