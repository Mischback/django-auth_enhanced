# -*- coding: utf-8 -*-
"""These tests target the URL configuration."""

# Python imports
from unittest import skip  # noqa

# Django imports
from django.test import override_settings, tag  # noqa
from django.urls import reverse

# app imports
from .utils.testcases import AEUrlTestCase


class UrlTests(AEUrlTestCase):
    """Tests targeting the app's URL configuration"""

    def test_login_url(self):
        """Can the URL be retrieved by its name and is the right function used?"""

        # get the URL by its name
        url = reverse('auth_enhanced:login')
        self.assertEqual(url, '/login/')

        self.assertFuncName('LoginView', url=url)
