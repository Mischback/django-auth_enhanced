# -*- coding: utf-8 -*-
"""Includes tests targeting the app-specific checks.

    - target file: auth_enhanced/checks.py
    - included tags: 'checks'

The app's checks rely on Django's system check framework."""

# Python imports
from unittest import skip  # noqa

# Django imports
from django.test import override_settings, tag  # noqa

# app imports
from auth_enhanced.checks import (
    E001, E002, E003, E004, E005, E006, E007, E008, W009, W010, W011,
    check_settings_values,
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

    @override_settings(DAE_EMAIL_LINK_SCHEME='http')
    def test_e004_valid(self):
        """Check should accept valid values."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [])

    @override_settings(DAE_EMAIL_LINK_SCHEME='ftp')
    def test_e004_invalid(self):
        """Invalid values show an error message."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [E004])

    @override_settings(DAE_EMAIL_ADMIN_LINK_SCHEME='http')
    def test_e005_valid(self):
        """Check should accept valid values."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [])

    @override_settings(DAE_EMAIL_ADMIN_LINK_SCHEME='ftp')
    def test_e005_invalid(self):
        """Invalid values show an error message."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [E005])

    @override_settings(DAE_EMAIL_ADMIN_NOTIFICATION_PREFIX='foo')
    def test_e006_valid(self):
        """Check should accept valid values."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [])

    @override_settings(DAE_EMAIL_ADMIN_NOTIFICATION_PREFIX=None)
    def test_e006_invalid(self):
        """Invalid values show an error message."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [E006])

    @override_settings(DAE_PROJECT_NAME='foo')
    def test_e007_valid(self):
        """Check should accept valid values."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [])

    @override_settings(DAE_PROJECT_NAME=None)
    def test_e007_invalid(self):
        """Invalid values show an error message."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [E007])

    @override_settings(DAE_EMAIL_HOME_VIEW_NAME='home')
    def test_e008_valid(self):
        """Check should accept valid values."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [])

    @override_settings(DAE_EMAIL_HOME_VIEW_NAME='really-not-existing-view-name')
    def test_e008_invalid(self):
        """Invalid values show an error message."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [E008])

    @override_settings(LOGIN_URL=DAE_CONST_RECOMMENDED_LOGIN_URL)
    def test_w009_valid(self):
        """Check should accept valid values."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [])

    @override_settings(LOGIN_URL='foo/')
    def test_w009_invalid(self):
        """Invalid values show an error message."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [W009])

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
    def test_w010_invalid(self):
        """Invalid values show an error message."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [W010])

    @override_settings(DAE_EMAIL_FROM_ADDRESS='foo@localhost')
    def test_w011_valid(self):
        """Check should accept valid values."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [])

    @override_settings(DAE_EMAIL_FROM_ADDRESS='foo')
    def test_w011_invalid(self):
        """Invalid values show an error message."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [W011])
