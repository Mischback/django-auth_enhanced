# -*- coding: utf-8 -*-
"""Includes tests targeting the app-specific checks.

    - target file: auth_enhanced/checks.py
    - included tags: 'checks'

The app's checks rely on Django's system check framework."""

# Python imports
from unittest import skip  # noqa

# Django imports
from django.contrib.auth.models import User
from django.test import override_settings, tag  # noqa

# app imports
from auth_enhanced.models import UserEnhancement

# app imports
from .utils.testcases import AuthEnhancedTestCase


class UserEnhancementTests(AuthEnhancedTestCase):
    """Tests targeting the model class."""

    def test_email_is_verified(self):
        """Does the boolean abstraction work?"""

        u = User(username='foo')
        ue = UserEnhancement(
            user=u,
            email_verification_status=UserEnhancement.EMAIL_VERIFICATION_COMPLETED
        )

        self.assertTrue(ue.email_is_verified)

        ue.email_verification_status = UserEnhancement.EMAIL_VERIFICATION_IN_PROGRESS
        self.assertFalse(ue.email_is_verified)

        ue.email_verification_status = UserEnhancement.EMAIL_VERIFICATION_FAILED
        self.assertFalse(ue.email_is_verified)
