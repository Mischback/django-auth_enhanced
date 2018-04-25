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
from auth_enhanced.checks import E001, E002, check_settings_values, W001
from auth_enhanced.settings import DAE_CONST_MODE_AUTO_ACTIVATION, DAE_CONST_RECOMMENDED_LOGIN_URL

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

    @override_settings(LOGIN_URL=DAE_CONST_RECOMMENDED_LOGIN_URL)
    def test_w001_valid(self):
        """Check should accept valid values."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [])

    @override_settings(LOGIN_URL='foo/')
    def test_w001_invalid(self):
        """Invalid values show an error message."""
        errors = check_settings_values(None)
        self.assertEqual(errors, [W001])
