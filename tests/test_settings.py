# -*- coding: utf-8 -*-
"""Includes tests targeting the app-specific settings.

    - target file: auth_enhanced/settings.py
    - included tags: 'settings'

Yeah, settings can't be tested properly. In fact, this file tests the utility
functions, that are used to inject these settings."""

# Python imports
from unittest import skip  # noqa

# Django imports
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings, tag  # noqa

# app imports
from auth_enhanced.exceptions import AuthEnhancedConversionError
from auth_enhanced.settings import convert_to_seconds, inject_setting

# app imports
from .utils.testcases import AuthEnhancedTestCase


@tag('settings')
class ConvertToSecondsTests(AuthEnhancedTestCase):
    """These tests target 'convert_to_seconds()'."""

    def test_value_hours(self):
        """A trailing 'h' causes the string to be read as 'hours'."""

        hours = 5
        self.assertEqual(convert_to_seconds('{}h'.format(hours)), hours * 3600)

    def test_value_days(self):
        """A trailing 'd' causes the string to be read as 'days'."""

        days = 5
        self.assertEqual(convert_to_seconds('{}d'.format(days)), days * 3600 * 24)

    def test_value_no_trailing_qualifier(self):
        """An integer wrapped in a string will be accepted."""

        seconds = 1338
        self.assertEqual(convert_to_seconds('{}'.format(seconds)), seconds)

    def test_value_mismatch(self):
        """Any trailing character other that 'h' or 'd' will raise an exception."""

        with self.assertRaisesMessage(
            AuthEnhancedConversionError,
            "Could not convert the parameter to an integer value."
        ):
            convert_to_seconds('42foo')

    def test_not_convertible_as_int(self):
        """If the reminder can not be converted to an int, an exception will be raised."""

        with self.assertRaisesMessage(
            AuthEnhancedConversionError,
            "Could not convert the parameter to an integer value."
        ):
            convert_to_seconds('food')


@tag('settings')
class InjectSettingTests(AuthEnhancedTestCase):
    """These tests target 'inject_setting()'."""

    def test_name_not_uppercase(self):
        """Non-uppercase setting names should be rejected."""

        with self.assertRaises(ImproperlyConfigured):
            inject_setting('foo', 'bar')

    @override_settings(FOO='keep-this-setting')
    def test_setting_already_set(self):
        """If the setting is already present, it should not be overwritten."""

        inject_setting('FOO', 'bar')
        self.assertNotEqual(settings.FOO, 'bar')
        self.assertEqual(settings.FOO, 'keep-this-setting')

    def test_setting_injection_working(self):
        """Is the setting successfully injected?"""

        inject_setting('FOO', 'bar')
        self.assertEqual(settings.FOO, 'bar')
