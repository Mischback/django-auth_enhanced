# -*- coding: utf-8 -*-
"""Includes tests targeting the app-specific URLs.

    - target file: auth_enhanced/urls.py
    - included tags: 'urls'

Please note, that these are very basic tests, that basically check the correct
resolution of named URLs to the correct view function / CBV."""

# Python imports
from unittest import skip  # noqa

# Django imports
from django.test import override_settings, tag  # noqa
from django.urls import reverse

# app imports
from .utils.testcases import AEUrlTestCase


@tag('urls')
class UrlTests(AEUrlTestCase):
    """Tests targeting the app's URL configuration"""

    def test_login_url(self):
        """Can the URL be retrieved by its name and is the right function used?"""

        # get the URL by its name
        url = reverse('auth_enhanced:login')
        self.assertEqual(url, '/login/')

        self.assertCBVName('LoginView', module='django.contrib.auth.views', url=url)

    def test_logout_url(self):
        """Can the URL be retrieved by its name and is the right function used?"""

        # get the URL by its name
        url = reverse('auth_enhanced:logout')
        self.assertEqual(url, '/logout/')

        self.assertCBVName('LogoutView', module='django.contrib.auth.views', url=url)

    def test_signup_url(self):
        """Can the URL be retrieved by its name and is the right function used?"""

        # get the URL by its name
        url = reverse('auth_enhanced:signup')
        self.assertEqual(url, '/signup/')

        self.assertCBVName('SignupView', module='auth_enhanced.views', url=url)

    def test_verify_email_url_no_token(self):
        """Can the URL be retrieved by its name and is the right function used?"""

        # get the URL by its name
        url = reverse('auth_enhanced:email-verification')
        self.assertEqual(url, '/verify-email/')

        self.assertCBVName('EmailVerificationView', module='auth_enhanced.views', url=url)

    def test_verify_email_url_with_token(self):
        """Can the URL be retrieved by its name and is the right function used?"""

        # get the URL by its name
        url = reverse('auth_enhanced:email-verification', kwargs={'verification_token': 'foo'})
        self.assertEqual(url, '/verify-email/foo/')

        self.assertCBVName('EmailVerificationView', module='auth_enhanced.views', url=url)
