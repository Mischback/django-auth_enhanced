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
from auth_enhanced.settings import inject_setting

# app imports
from .utils.testcases import AuthEnhancedNoSignalsTestCase


@tag('settings')
class InjectSettingTests(AuthEnhancedNoSignalsTestCase):
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
