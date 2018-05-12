# -*- coding: utf-8 -*-
"""Includes tests targeting the app-specific admin classes.

    - target file: auth_enhanced/admin.py
    - included tags: 'admin'"""

# Python imports
from unittest import skip  # noqa

# Django imports
from django.contrib.auth import get_user_model
from django.test import override_settings, tag  # noqa

# app imports
from auth_enhanced.admin import EnhancedUserAdmin, EnhancedUserStatusFilter

# app imports
from .utils.testcases import AuthEnhancedTestCase


@tag('admin')
class EnhancedUserStatusFilterTest(AuthEnhancedTestCase):
    """These tests target the custom status filter."""

    fixtures = ['tests/utils/fixtures/test_different_users.json']

    def test_filter_superusers(self):
        """Does the filter return the superusers?"""

        f = EnhancedUserStatusFilter(None, {'status': 'superusers'}, get_user_model(), EnhancedUserAdmin)
        f_result = f.queryset(None, get_user_model().objects.all())

        # number of superusers in fixture is subject to changes!
        self.assertEqual(len(f_result), 3)

    def test_filter_staffusers(self):
        """Does the filter return the staff users?"""

        f = EnhancedUserStatusFilter(None, {'status': 'staff'}, get_user_model(), EnhancedUserAdmin)
        f_result = f.queryset(None, get_user_model().objects.all())

        # number of superusers in fixture is subject to changes!
        self.assertEqual(len(f_result), 5)

    def test_filter_users(self):
        """Does the filter return the default users?"""

        f = EnhancedUserStatusFilter(None, {'status': 'users'}, get_user_model(), EnhancedUserAdmin)
        f_result = f.queryset(None, get_user_model().objects.all())

        # number of superusers in fixture is subject to changes!
        self.assertEqual(len(f_result), 1)

    def test_filter_no_filter(self):
        """If the filter is not applied, return the full user list."""

        f = EnhancedUserStatusFilter(None, {}, get_user_model(), EnhancedUserAdmin)
        f_result = f.queryset(None, get_user_model().objects.all())

        # number of superusers in fixture is subject to changes!
        self.assertEqual(len(f_result), 6)
