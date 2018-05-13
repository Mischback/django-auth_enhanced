# -*- coding: utf-8 -*-
"""Includes tests targeting the app-specific admin classes.

    - target file: auth_enhanced/admin.py
    - included tags: 'admin'"""

# Python imports
from unittest import skip  # noqa

# Django imports
from django.conf import settings
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


@tag('admin')
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

    @override_settings(DAE_ADMIN_USERNAME_STATUS_COLOR=None)
    def test_username_status_color_missing_setting(self):
        """Just returns the username, if no colors are specified."""

        # actually delete the setting
        #   Please note, how the setting is first overridden and then deleted.
        #   This is done to ensure, that this works independently from the
        #   test settings.
        del settings.DAE_ADMIN_USERNAME_STATUS_COLOR

        u = get_user_model().objects.get(username='django')
        self.assertEqual(
            self.admin_obj.username_status_color(u), getattr(u, u.USERNAME_FIELD)
        )

    @override_settings(DAE_ADMIN_USERNAME_STATUS_COLOR=('#0f0f0f', '#f0f0f0'))
    def test_username_status_color_user(self):
        """Just returns the username, if it is a normal user."""

        u = get_user_model().objects.get(username='baz')
        self.assertEqual(
            self.admin_obj.username_status_color(u), getattr(u, u.USERNAME_FIELD)
        )

    @override_settings(DAE_ADMIN_USERNAME_STATUS_COLOR=('#0f0f0f', '#f0f0f0'))
    def test_username_status_color_staff(self):
        """Applies a color to the username, if staff status."""

        u = get_user_model().objects.get(username='staff_user1')
        self.assertEqual(
            self.admin_obj.username_status_color(u),
            '<span style="color: {};">{}</span>'.format(
                '#f0f0f0',
                getattr(u, u.USERNAME_FIELD)
            )
        )

    @override_settings(DAE_ADMIN_USERNAME_STATUS_COLOR=('#0f0f0f', '#f0f0f0'))
    def test_username_status_color_superuser(self):
        """Applies a color to the username, if superuser status."""

        u = get_user_model().objects.get(username='django')
        self.assertEqual(
            self.admin_obj.username_status_color(u),
            '<span style="color: {};">{}</span>'.format(
                '#0f0f0f',
                getattr(u, u.USERNAME_FIELD)
            )
        )

    @override_settings(DAE_ADMIN_USERNAME_STATUS_CHAR=None)
    def test_username_status_char_missing_setting(self):
        """Just returns the username, if no colors are specified."""

        # actually delete the setting
        #   Please note, how the setting is first overridden and then deleted.
        #   This is done to ensure, that this works independently from the
        #   test settings.
        del settings.DAE_ADMIN_USERNAME_STATUS_CHAR

        u = get_user_model().objects.get(username='django')
        self.assertEqual(
            self.admin_obj.username_status_char(u), getattr(u, u.USERNAME_FIELD)
        )

    @override_settings(DAE_ADMIN_USERNAME_STATUS_CHAR=('a', 'b'))
    def test_username_status_char_user(self):
        """Just returns the username, if it is a normal user."""

        u = get_user_model().objects.get(username='baz')
        self.assertEqual(
            self.admin_obj.username_status_char(u), getattr(u, u.USERNAME_FIELD)
        )

    @override_settings(DAE_ADMIN_USERNAME_STATUS_CHAR=('a', 'b'))
    def test_username_status_char_staff(self):
        """Applies a color to the username, if staff status."""

        u = get_user_model().objects.get(username='staff_user1')
        self.assertEqual(
            self.admin_obj.username_status_char(u),
            '[{}]{}'.format('b', getattr(u, u.USERNAME_FIELD))
        )

    @override_settings(DAE_ADMIN_USERNAME_STATUS_CHAR=('a', 'b'))
    def test_username_status_char_superuser(self):
        """Applies a color to the username, if superuser status."""

        u = get_user_model().objects.get(username='django')
        self.assertEqual(
            self.admin_obj.username_status_char(u),
            '[{}]{}'.format('a', getattr(u, u.USERNAME_FIELD))
        )


class EnhancedUserAdminTests(AuthEnhancedTestCase):

    def setUp(self):
        """Per test setup"""

        # create an instance of the admin class
        self.admin_obj = EnhancedUserAdmin(get_user_model(), AdminSite())

    @override_settings(DAE_ADMIN_USERNAME_STATUS_CHAR=('a', 'b'))
    def test_get_legend_char(self):
        """Is the legend properly populated?"""

        # override 'list_display' per test
        self.admin_obj.list_display = ('username_status_char', )

        self.assertEqual(
            self.admin_obj.get_additional_legend(),
            {'char': ('a', 'b')}
        )

    @override_settings(DAE_ADMIN_USERNAME_STATUS_CHAR=None)
    def test_get_legend_char_missing_setting(self):
        """Legend remains empty, if the corresponding setting is missing."""

        # override 'list_display' per test
        self.admin_obj.list_display = ('username_status_char', )

        # actually delete the setting
        #   Please note, how the setting is first overridden and then deleted.
        #   This is done to ensure, that this works independently from the
        #   test settings.
        del settings.DAE_ADMIN_USERNAME_STATUS_CHAR

        self.assertEqual(
            self.admin_obj.get_additional_legend(),
            {}
        )

    @override_settings(DAE_ADMIN_USERNAME_STATUS_COLOR=('#f0f0f0', '#0f0f0f'))
    def test_get_legend_color(self):
        """Is the legend properly populated?"""

        # override 'list_display' per test
        self.admin_obj.list_display = ('username_status_color', )

        self.assertEqual(
            self.admin_obj.get_additional_legend(),
            {'color': ('#f0f0f0', '#0f0f0f')}
        )

    @override_settings(DAE_ADMIN_USERNAME_STATUS_COLOR=None)
    def test_get_legend_color_missing_setting(self):
        """Legend remains empty, if the corresponding setting is missing."""

        # override 'list_display' per test
        self.admin_obj.list_display = ('username_status_color', )

        # actually delete the setting
        #   Please note, how the setting is first overridden and then deleted.
        #   This is done to ensure, that this works independently from the
        #   test settings.
        del settings.DAE_ADMIN_USERNAME_STATUS_COLOR

        self.assertEqual(
            self.admin_obj.get_additional_legend(),
            {}
        )
