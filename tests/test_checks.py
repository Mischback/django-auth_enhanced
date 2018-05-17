# -*- coding: utf-8 -*-
"""Includes tests targeting the app-specific checks.

    - target file: auth_enhanced/checks.py
    - included tags: 'checks'

The app's checks rely on Django's system check framework."""

# Python imports
from unittest import skip  # noqa

# Django imports
from django.conf import settings
from django.test import override_settings, tag  # noqa

# app imports
from auth_enhanced.checks import (
    E001, E002, E003, E004, E008, E009, E010, E011, E012, E013, W005, W006,
    W007, check_settings_values,
)
from auth_enhanced.settings import (
    DAE_CONST_MODE_AUTO_ACTIVATION, DAE_CONST_RECOMMENDED_LOGIN_URL,
)

# app imports
from .utils.testcases import AuthEnhancedTestCase


@tag('checks')
class CheckSettingsValuesTests(AuthEnhancedTestCase):
    """These tests target 'check_settings_values()'."""

    @override_settings(DAE_OPERATION_MODE=DAE_CONST_MODE_AUTO_ACTIVATION)
    def test_e001_valid(self):
        """Check should accept valid values."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [])

    @override_settings(DAE_OPERATION_MODE='foo')
    def test_e001_invalid(self):
        """Invalid values show an error message."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [E001])

    @override_settings(DAE_EMAIL_TEMPLATE_PREFIX='foo')
    def test_e002_valid(self):
        """Check should accept valid values."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [])

    @override_settings(DAE_EMAIL_TEMPLATE_PREFIX='foo/')
    def test_e002_invalid(self):
        """Invalid values show an error message."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [E002])

    @override_settings(DAE_ADMIN_SIGNUP_NOTIFICATION=False)
    def test_e003_valid_false(self):
        """Check should accept valid values."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [])

    @override_settings(DAE_ADMIN_SIGNUP_NOTIFICATION=(('foo', 'foo@localhost', ('mail', )), ))
    def test_e003_valid_list(self):
        """Check should accept valid values."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [])

    @override_settings(DAE_ADMIN_SIGNUP_NOTIFICATION=True)
    def test_e003_invalid_bool_true(self):
        """Invalid values show an error message."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [E003])

    @override_settings(DAE_ADMIN_SIGNUP_NOTIFICATION=(('foo', 'foo', ('mail', )), ))
    def test_e003_invalid_no_valid_mail_address(self):
        """Invalid values show an error message."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [E003])

    @override_settings(DAE_ADMIN_SIGNUP_NOTIFICATION=(('foo', 'foo@localhost', ('liam', )), ))
    def test_e003_invalid_no_valid_notification_method(self):
        """Invalid values show an error message."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [E003])

    @override_settings(DAE_EMAIL_ADMIN_NOTIFICATION_PREFIX='foo')
    def test_e004_valid(self):
        """Check should accept valid values."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [])

    @override_settings(DAE_EMAIL_ADMIN_NOTIFICATION_PREFIX=None)
    def test_e004_invalid(self):
        """Invalid values show an error message."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [E004])

    @override_settings(LOGIN_URL=DAE_CONST_RECOMMENDED_LOGIN_URL)
    def test_w005_valid(self):
        """Check should accept valid values."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [])

    @override_settings(LOGIN_URL='foo/')
    def test_w005_invalid(self):
        """Invalid values show an error message."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [W005])

    @override_settings(
        EMAIL_HOST='localhost',
        EMAIL_PORT=25,
        EMAIL_HOST_USER='',
        EMAIL_HOST_PASSWORD='',
        EMAIL_USE_TLS=False,
        EMAIL_USE_SSL=False,
        EMAIL_TIMEOUT=None,
        EMAIL_SSL_KEYFILE=None,
        EMAIL_SSL_CERTFILE=None,
        EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
    )
    def test_w006_invalid(self):
        """Invalid values show an error message."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [W006])

    @override_settings(DAE_EMAIL_FROM_ADDRESS='foo@localhost')
    def test_w007_valid(self):
        """Check should accept valid values."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [])

    @override_settings(DAE_EMAIL_FROM_ADDRESS='foo')
    def test_w007_invalid(self):
        """Invalid values show an error message."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [W007])

    @override_settings(DAE_EMAIL_PREFIX='foo')
    def test_e008_valid(self):
        """Check should accept valid values."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [])

    @override_settings(DAE_EMAIL_PREFIX=None)
    def test_e008_invalid(self):
        """Invalid values show an error message."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [E008])

    @override_settings(DAE_SALT='foo')
    def test_e009_valid(self):
        """Check should accept valid values."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [])

    @override_settings(DAE_SALT=None)
    def test_e009_invalid(self):
        """Invalid values show an error message."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [E009])

    @override_settings(DAE_VERIFICATION_TOKEN_MAX_AGE=1338)
    def test_e010_valid(self):
        """Check should accept valid values."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [])

    @override_settings(DAE_VERIFICATION_TOKEN_MAX_AGE=None)
    def test_e010_invalid(self):
        """Invalid values show an error message.

        Actually, 'None' is the only way to raise this error."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [E010])

    @skip('currently inactive')
    @override_settings(DAE_ADMIN_SHOW_SEARCHBOX=True)
    def test_e011_valid(self):
        """Check should accept valid values."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [])

    @skip('currently inactive')
    @override_settings(DAE_ADMIN_SHOW_SEARCHBOX='foo')
    def test_e011_invalid(self):
        """Invalid values show an error message."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [E011])

    @override_settings(DAE_ADMIN_USERNAME_STATUS_COLOR=('#0f0f0f', '#f0f0f0'))
    def test_e012_valid(self):
        """Check should accept valid values."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [])

    @override_settings(DAE_ADMIN_USERNAME_STATUS_COLOR=None)
    def test_e012_missing_setting(self):
        """Missing setting will be ignored."""

        # actually delete the setting
        #   Please note, how the setting is first overridden and then deleted.
        #   This is done to ensure, that this works independently from the
        #   test settings.
        del settings.DAE_ADMIN_USERNAME_STATUS_COLOR

        errors = check_settings_values(None)
        self.assertEqual(errors, [])

    @override_settings(DAE_ADMIN_USERNAME_STATUS_COLOR='foo')
    def test_e012_invalid_no_tuple(self):
        """Invalid values show an error message."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [E012])

    @override_settings(DAE_ADMIN_USERNAME_STATUS_COLOR=('foo', 'bar', 'baz'))
    def test_e012_invalid_invalid_number_of_parameters(self):
        """Invalid values show an error message."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [E012])

    @override_settings(DAE_ADMIN_USERNAME_STATUS_COLOR=('foo', 'bar'))
    def test_e012_invalid_no_color_codes(self):
        """Invalid values show an error message."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [E012])

    @override_settings(DAE_ADMIN_USERNAME_STATUS_CHAR=('#', '$'))
    def test_e013_valid(self):
        """Check should accept valid values."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [])

    @override_settings(DAE_ADMIN_USERNAME_STATUS_CHAR=None)
    def test_e013_missing_setting(self):
        """Missing setting will be ignored."""

        # actually delete the setting
        #   Please note, how the setting is first overridden and then deleted.
        #   This is done to ensure, that this works independently from the
        #   test settings.
        del settings.DAE_ADMIN_USERNAME_STATUS_CHAR

        errors = check_settings_values(None)
        self.assertEqual(errors, [])

    @override_settings(DAE_ADMIN_USERNAME_STATUS_CHAR='foo')
    def test_e013_invalid_no_tuple(self):
        """Invalid values show an error message."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [E013])

    @override_settings(DAE_ADMIN_USERNAME_STATUS_CHAR=('#', '$', '!'))
    def test_e013_invalid_invalid_number_of_parameters(self):
        """Invalid values show an error message."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [E013])

    @override_settings(DAE_ADMIN_USERNAME_STATUS_CHAR=('foo', 'bar'))
    def test_e013_invalid_no_color_codes(self):
        """Invalid values show an error message."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [E013])
