# -*- coding: utf-8 -*-
"""Includes tests targeting the app-specific admin classes.

    - target file: auth_enhanced/admin.py
    - included tags: 'admin'"""

# Python imports
from unittest import skip  # noqa

# Django imports
from django.conf import settings
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.templatetags.admin_list import _boolean_icon
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import override_settings, tag  # noqa
from django.urls import reverse

# app imports
from auth_enhanced.admin import EnhancedUserAdmin, EnhancedUserStatusFilter
from auth_enhanced.settings import (
    DAE_CONST_MODE_EMAIL_ACTIVATION, DAE_CONST_MODE_MANUAL_ACTIVATION,
)

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
        self.assertEqual(len(f_result), 7)

    def test_filter_staffusers(self):
        """Does the filter return the staff users?"""

        f = EnhancedUserStatusFilter(None, {'status': 'staff'}, get_user_model(), EnhancedUserAdmin)
        f_result = f.queryset(None, get_user_model().objects.all())

        # number of superusers in fixture is subject to changes!
        self.assertEqual(len(f_result), 13)

    def test_filter_users(self):
        """Does the filter return the default users?"""

        f = EnhancedUserStatusFilter(None, {'status': 'users'}, get_user_model(), EnhancedUserAdmin)
        f_result = f.queryset(None, get_user_model().objects.all())

        # number of superusers in fixture is subject to changes!
        self.assertEqual(len(f_result), 6)

    def test_filter_no_filter(self):
        """If the filter is not applied, return the full user list."""

        f = EnhancedUserStatusFilter(None, {}, get_user_model(), EnhancedUserAdmin)
        f_result = f.queryset(None, get_user_model().objects.all())

        # number of superusers in fixture is subject to changes!
        self.assertEqual(len(f_result), 19)


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

        u = get_user_model().objects.get(username='user')
        self.assertEqual(self.admin_obj.status_aggregated(u), 'user')

    def test_status_aggregated_staff(self):
        """Does the method returns the correct status for staff users?"""

        u = get_user_model().objects.get(username='staff')
        self.assertEqual(self.admin_obj.status_aggregated(u), 'staff')

    def test_status_aggregated_superuser(self):
        """Does the method returns the correct status for superusers?"""

        u = get_user_model().objects.get(username='superuser')
        self.assertEqual(self.admin_obj.status_aggregated(u), 'superuser')

    @override_settings(DAE_ADMIN_USERNAME_STATUS_COLOR=None)
    def test_username_status_color_missing_setting(self):
        """Just returns the username, if no colors are specified."""

        # actually delete the setting
        #   Please note, how the setting is first overridden and then deleted.
        #   This is done to ensure, that this works independently from the
        #   test settings.
        del settings.DAE_ADMIN_USERNAME_STATUS_COLOR

        u = get_user_model().objects.get(username='superuser')
        self.assertEqual(
            self.admin_obj.username_status_color(u), getattr(u, u.USERNAME_FIELD)
        )

    @override_settings(DAE_ADMIN_USERNAME_STATUS_COLOR=('#0f0f0f', '#f0f0f0'))
    def test_username_status_color_user(self):
        """Just returns the username, if it is a normal user."""

        u = get_user_model().objects.get(username='user')
        self.assertEqual(
            self.admin_obj.username_status_color(u), getattr(u, u.USERNAME_FIELD)
        )

    @override_settings(DAE_ADMIN_USERNAME_STATUS_COLOR=('#0f0f0f', '#f0f0f0'))
    def test_username_status_color_staff(self):
        """Applies a color to the username, if staff status."""

        u = get_user_model().objects.get(username='staff')
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

        u = get_user_model().objects.get(username='superuser')
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

        u = get_user_model().objects.get(username='superuser')
        self.assertEqual(
            self.admin_obj.username_status_char(u), getattr(u, u.USERNAME_FIELD)
        )

    @override_settings(DAE_ADMIN_USERNAME_STATUS_CHAR=('a', 'b'))
    def test_username_status_char_user(self):
        """Just returns the username, if it is a normal user."""

        u = get_user_model().objects.get(username='user')
        self.assertEqual(
            self.admin_obj.username_status_char(u), getattr(u, u.USERNAME_FIELD)
        )

    @override_settings(DAE_ADMIN_USERNAME_STATUS_CHAR=('a', 'b'))
    def test_username_status_char_staff(self):
        """Applies a color to the username, if staff status."""

        u = get_user_model().objects.get(username='staff')
        self.assertEqual(
            self.admin_obj.username_status_char(u),
            '[{}]{}'.format('b', getattr(u, u.USERNAME_FIELD))
        )

    @override_settings(DAE_ADMIN_USERNAME_STATUS_CHAR=('a', 'b'))
    def test_username_status_char_superuser(self):
        """Applies a color to the username, if superuser status."""

        u = get_user_model().objects.get(username='superuser')
        self.assertEqual(
            self.admin_obj.username_status_char(u),
            '[{}]{}'.format('a', getattr(u, u.USERNAME_FIELD))
        )

    def test_toggle_is_active(self):
        """Should display an activation button for inactive users and a
        deactivation button for active users."""

        u = get_user_model().objects.get(username='user')
        self.assertIn(
            'deactivate',
            self.admin_obj.toggle_is_active(u)
        )

        u = get_user_model().objects.get(username='user1')
        self.assertIn(
            'activate',
            self.admin_obj.toggle_is_active(u)
        )

    def test_is_active_with_action(self):
        """Should display a Django icon with the button from 'toggle_is_active'."""

        u = get_user_model().objects.get(username='user')
        retval = self.admin_obj.is_active_with_action(u)
        self.assertIn('deactivate', retval)
        self.assertIn(_boolean_icon(u.is_active), retval)

        u = get_user_model().objects.get(username='user1')
        retval = self.admin_obj.is_active_with_action(u)
        self.assertIn('activate', retval)
        self.assertIn(_boolean_icon(u.is_active), retval)

    def test_email_with_verification_status(self):
        """Should display the user's email address and its verification status."""

        u = get_user_model().objects.get(username='user')
        retval = self.admin_obj.email_with_verification_status(u)
        self.assertIn(getattr(u, u.EMAIL_FIELD), retval)
        self.assertIn(_boolean_icon(u.enhancement.email_is_verified), retval)

        u = get_user_model().objects.get(username='user_not_verified')
        retval = self.admin_obj.email_with_verification_status(u)
        self.assertIn(getattr(u, u.EMAIL_FIELD), retval)
        self.assertIn(_boolean_icon(u.enhancement.email_is_verified), retval)


@tag('admin')
class EnhancedUserAdminTests(AuthEnhancedTestCase):
    """These tests target the admin class, but do not require any user objects."""

    def setUp(self):
        """Per test setup"""

        super(EnhancedUserAdminTests, self).setUp()

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


@tag('admin')
class EnhancedUserAdminRequestsTests(AuthEnhancedTestCase):
    """These tests target the admin class, but rely on real requests."""

    fixtures = ['tests/utils/fixtures/test_different_users.json']

    def setUp(self):

        super(EnhancedUserAdminRequestsTests, self).setUp()

        self.user_model = get_user_model()
        self.content_type = ContentType.objects.get_for_model(self.user_model)
        self.client.force_login(self.user_model.objects.get(username='superuser'))

    @override_settings(DAE_OPERATION_MODE=DAE_CONST_MODE_MANUAL_ACTIVATION)
    def test_action_bulk_activate_single_user(self):
        """Activate a single user by dropdown."""

        u = self.user_model.objects.get(username='user1')

        # check, if the user is inactive
        self.assertFalse(u.is_active)

        # try to activate a single user
        action_data = {
            ACTION_CHECKBOX_NAME: [u.pk],
            'action': 'action_bulk_activate_user'
        }
        response = self.client.post(
            reverse('admin:{}_{}_changelist'.format(self.content_type.app_label, self.content_type.model)),
            action_data,
            follow=True
        )

        # user should now be active
        self.assertTrue(self.user_model.objects.get(username='user1').is_active)

        # message indicates the activation of 1 user
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), '1 user was activated successfully (user1).')

    @override_settings(DAE_OPERATION_MODE=DAE_CONST_MODE_MANUAL_ACTIVATION)
    def test_action_bulk_activate_multiple_users(self):
        """Activate a multiple users by dropdown."""

        u = self.user_model.objects.get(username='user1')
        v = self.user_model.objects.get(username='user2')

        # check, if the user is inactive
        self.assertFalse(u.is_active)
        self.assertFalse(v.is_active)

        # try to activate a single user
        action_data = {
            ACTION_CHECKBOX_NAME: [u.pk, v.pk],
            'action': 'action_bulk_activate_user'
        }
        response = self.client.post(
            reverse('admin:{}_{}_changelist'.format(self.content_type.app_label, self.content_type.model)),
            action_data,
            follow=True
        )

        # user should now be active
        self.assertTrue(self.user_model.objects.get(username='user1').is_active)
        self.assertTrue(self.user_model.objects.get(username='user2').is_active)

        # message indicates the activation of 1 user
        messages = list(response.wsgi_request._messages)
        self.assertIn('2 users were activated successfully', str(messages[0]))
        self.assertIn('user1', str(messages[0]))
        self.assertIn('user2', str(messages[0]))

    @override_settings(DAE_OPERATION_MODE=DAE_CONST_MODE_EMAIL_ACTIVATION)
    def test_action_bulk_activate_single_user_fail(self):
        """Activate a single user by dropdown."""

        u = self.user_model.objects.get(username='user2')

        # check, if the user is inactive
        self.assertFalse(u.is_active)

        # try to activate a single user
        action_data = {
            ACTION_CHECKBOX_NAME: [u.pk],
            'action': 'action_bulk_activate_user'
        }
        response = self.client.post(
            reverse('admin:{}_{}_changelist'.format(self.content_type.app_label, self.content_type.model)),
            action_data,
            follow=True
        )

        # user should now be active
        self.assertFalse(self.user_model.objects.get(username='user2').is_active)

        # message indicates the activation of 1 user
        messages = list(response.wsgi_request._messages)
        self.assertEqual(
            str(messages[0]),
            "1 user could not be activated, because his email address is not "
            "verified (user2)!"
        )

    @override_settings(DAE_OPERATION_MODE=DAE_CONST_MODE_EMAIL_ACTIVATION)
    def test_action_bulk_activate_multiple_users_fail(self):
        """Activate a multiple users by dropdown."""

        u = self.user_model.objects.get(username='user2')
        v = self.user_model.objects.get(username='user3')

        # check, if the user is inactive
        self.assertFalse(u.is_active)
        self.assertFalse(v.is_active)

        # try to activate a single user
        action_data = {
            ACTION_CHECKBOX_NAME: [u.pk, v.pk],
            'action': 'action_bulk_activate_user'
        }
        response = self.client.post(
            reverse('admin:{}_{}_changelist'.format(self.content_type.app_label, self.content_type.model)),
            action_data,
            follow=True
        )

        # user should now be active
        self.assertFalse(self.user_model.objects.get(username='user2').is_active)
        self.assertFalse(self.user_model.objects.get(username='user3').is_active)

        # message indicates the activation of 1 user
        messages = list(response.wsgi_request._messages)
        self.assertIn(
            "2 users could not be activated, because their email addresses are "
            "not verified",
            str(messages[0]),
        )
        self.assertIn('user2', str(messages[0]))
        self.assertIn('user3', str(messages[0]))

    @override_settings(DAE_OPERATION_MODE=DAE_CONST_MODE_EMAIL_ACTIVATION)
    def test_action_bulk_activate_invalid(self):
        """Activate a multiple users by dropdown."""

        # try to activate a single user
        action_data = {
            ACTION_CHECKBOX_NAME: [1338],
            'action': 'action_bulk_activate_user'
        }
        response = self.client.post(
            reverse('admin:{}_{}_changelist'.format(self.content_type.app_label, self.content_type.model)),
            action_data,
            follow=True
        )

        # message indicates the activation of 1 user
        messages = list(response.wsgi_request._messages)
        self.assertEqual(
            str(messages[0]),
            'Nothing was done. Probably this means, that no or invalid user IDs were provided.'
        )

    def test_action_bulk_deactivate_single_user(self):
        """Deactivate a single user by dropdown."""

        u = self.user_model.objects.get(username='user')

        # check, if the user is inactive
        self.assertTrue(u.is_active)

        # try to activate a single user
        action_data = {
            ACTION_CHECKBOX_NAME: [u.pk],
            'action': 'action_bulk_deactivate_user'
        }
        response = self.client.post(
            reverse('admin:{}_{}_changelist'.format(self.content_type.app_label, self.content_type.model)),
            action_data,
            follow=True
        )

        # user should now be active
        self.assertFalse(self.user_model.objects.get(username='user').is_active)

        # message indicates the activation of 1 user
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), '1 user was deactivated successfully (user).')

    def test_action_bulk_deactivate_multiple_users(self):
        """Deactivate a multiple users by dropdown."""

        u = self.user_model.objects.get(username='user')
        v = self.user_model.objects.get(username='user_in_progress')

        # check, if the user is inactive
        self.assertTrue(u.is_active)
        self.assertTrue(v.is_active)

        # try to activate a single user
        action_data = {
            ACTION_CHECKBOX_NAME: [u.pk, v.pk],
            'action': 'action_bulk_deactivate_user'
        }
        response = self.client.post(
            reverse('admin:{}_{}_changelist'.format(self.content_type.app_label, self.content_type.model)),
            action_data,
            follow=True
        )

        # user should now be active
        self.assertFalse(self.user_model.objects.get(username='user').is_active)
        self.assertFalse(self.user_model.objects.get(username='user_in_progress').is_active)

        # message indicates the activation of 1 user
        messages = list(response.wsgi_request._messages)
        self.assertIn('2 users were deactivated successfully', str(messages[0]))
        self.assertIn('user', str(messages[0]))
        self.assertIn('user_in_progress', str(messages[0]))

    def test_action_bulk_deactivate_single_user_fail(self):
        """Deactivate a single user by dropdown."""

        u = self.user_model.objects.get(username='superuser')

        # check, if the user is inactive
        self.assertTrue(u.is_active)

        # try to activate a single user
        action_data = {
            ACTION_CHECKBOX_NAME: [u.pk],
            'action': 'action_bulk_deactivate_user'
        }
        response = self.client.post(
            reverse('admin:{}_{}_changelist'.format(self.content_type.app_label, self.content_type.model)),
            action_data,
            follow=True
        )

        # user should still be active
        self.assertTrue(self.user_model.objects.get(username='superuser').is_active)

        # message indicates the activation of 1 user
        messages = list(response.wsgi_request._messages)
        self.assertEqual(
            str(messages[0]),
            "1 user could not be deactivated, because this is your own account (superuser)!"
        )

    def test_action_bulk_deactivate_invalid(self):
        """Deactivate a multiple users by dropdown."""

        # try to activate a single user
        action_data = {
            ACTION_CHECKBOX_NAME: [1338],
            'action': 'action_bulk_deactivate_user'
        }
        response = self.client.post(
            reverse('admin:{}_{}_changelist'.format(self.content_type.app_label, self.content_type.model)),
            action_data,
            follow=True
        )

        # message indicates the activation of 1 user
        messages = list(response.wsgi_request._messages)
        self.assertEqual(
            str(messages[0]),
            'Nothing was done. Probably this means, that no or invalid user IDs were provided.'
        )

    @override_settings(DAE_OPERATION_MODE=DAE_CONST_MODE_MANUAL_ACTIVATION)
    def test_action_activate_user_valid(self):
        """Activate a single user by button (pass to bulk method)."""

        u = self.user_model.objects.get(username='user1')

        # check, if the user is inactive
        self.assertFalse(u.is_active)

        # activate the user (by 'clicking' the button)
        response = self.client.get(reverse('admin:enhanced-activate-user', args=[u.pk]))

        # the user should be active
        self.assertTrue(self.user_model.objects.get(username='user1').is_active)

        # message indicates the activation of 1 user
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), '1 user was activated successfully (user1).')

    @override_settings(DAE_OPERATION_MODE=DAE_CONST_MODE_MANUAL_ACTIVATION)
    def test_action_activate_user_invalid(self):
        """Invalid user IDs are handled with a simple message."""

        # spoof an invalid user ID
        response = self.client.get(reverse('admin:enhanced-activate-user', args=[1338]))

        # message indicates, that no user got activated
        messages = list(response.wsgi_request._messages)
        self.assertEqual(
            str(messages[0]),
            'Nothing was done. Probably this means, that no or invalid user IDs were provided.'
        )

    def test_action_deactivate_user_valid(self):
        """Deactivate a single user by button (pass to bulk method)."""

        u = self.user_model.objects.get(username='user')

        # check, if the user is inactive
        self.assertTrue(u.is_active)

        # activate the user (by 'clicking' the button)
        response = self.client.get(reverse('admin:enhanced-deactivate-user', args=[u.pk]))

        # the user should be active
        self.assertFalse(self.user_model.objects.get(username='user').is_active)

        # message indicates the activation of 1 user
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), '1 user was deactivated successfully (user).')

    def test_action_deactivate_user_invalid(self):
        """Invalid user IDs are handled with a simple message."""

        # spoof an invalid user ID
        response = self.client.get(reverse('admin:enhanced-deactivate-user', args=[1338]))

        # message indicates, that no user got activated
        messages = list(response.wsgi_request._messages)
        self.assertEqual(
            str(messages[0]),
            'Nothing was done. Probably this means, that no or invalid user IDs were provided.'
        )
