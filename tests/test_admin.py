# -*- coding: utf-8 -*-
"""Includes tests targeting the app-specific admin classes.

    - target file: auth_enhanced/admin.py
    - included tags: 'admin'"""

# Python imports
from unittest import skip  # noqa

# Django imports
from django.contrib.admin.sites import AdminSite
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


@tag('admin', 'current')
class EnhancedUserAdminUserRelatedTests(AuthEnhancedTestCase):
    """These tests target the admin class and require some user objects."""

    fixtures = ['tests/utils/fixtures/test_different_users.json']

    @classmethod
    def setUpClass(cls):
        """Basic setup"""

        # call the parent constructor
        super(EnhancedUserAdminUserRelatedTests, cls).setUpClass()

        cls.admin_obj = EnhancedUserAdmin(get_user_model(), AdminSite())

    def test_status_aggregated_user(self):
        """Does the method returns the correct status for simple users?"""

        u = get_user_model().objects.get(username='baz')
        self.assertEqual(self.admin_obj.status_aggregated(u), 'user')

    def test_status_aggregated_staff(self):
        """Does the method returns the correct status for staff users?"""

        u = get_user_model().objects.get(username='staff_user1')
        self.assertEqual(self.admin_obj.status_aggregated(u), 'staff')

    def test_status_aggregated_superuser(self):
        """Does the method returns the correct status for superusers?"""

        u = get_user_model().objects.get(username='django')
        self.assertEqual(self.admin_obj.status_aggregated(u), 'superuser')
