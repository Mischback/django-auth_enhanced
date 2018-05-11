# -*- coding: utf-8 -*-
"""Includes tests targeting the app's management commands.

    - target file: auth_enhanced/management/commands/_lib.py
    - included tags: 'command'"""


# Python imports
from unittest import skip  # noqa

# Django imports
from django.contrib.auth import get_user_model
from django.core.management import CommandError, call_command
from django.test import override_settings, tag  # noqa

# app imports
from auth_enhanced.models import UserEnhancement

# app imports
from .utils.testcases import AuthEnhancedTestCase

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


@tag('command')
class CheckAdminNotificationTests(AuthEnhancedTestCase):
    """These tests target the 'check_admin_notification()'-function.

    See auth_enhanced/management/commands/_lib.py

    FIXME: Get rid of the setUp()-method and include the stuff into a fixture."""

    def setUp(self):

        # prepare test environment to capture stdout
        self.out = StringIO()

        user_model = get_user_model()

        # two fully valid superusers
        u = user_model.objects.create_superuser(**{
            user_model.USERNAME_FIELD: 'django',
            user_model.EMAIL_FIELD: 'django@localhost',
            'password': 'foo'
        })
        UserEnhancement.objects.create(
            user=u,
            email_verification_status=UserEnhancement.EMAIL_VERIFICATION_COMPLETED
        )
        v = user_model.objects.create_superuser(**{
            user_model.USERNAME_FIELD: 'foo',
            user_model.EMAIL_FIELD: 'foo@localhost',
            'password': 'foo'
        })
        UserEnhancement.objects.create(
            user=v,
            email_verification_status=UserEnhancement.EMAIL_VERIFICATION_COMPLETED
        )

        # superuser without verified email address
        w = user_model.objects.create_superuser(**{
            user_model.USERNAME_FIELD: 'bar',
            user_model.EMAIL_FIELD: 'bar@localhost',
            'password': 'foo'
        })
        UserEnhancement.objects.create(
            user=w,
            email_verification_status=UserEnhancement.EMAIL_VERIFICATION_FAILED
        )

        # a non-superuser
        x = user_model.objects.create_user(**{
            user_model.USERNAME_FIELD: 'baz',
            user_model.EMAIL_FIELD: 'baz@localhost',
            'password': 'foo'
        })
        UserEnhancement.objects.create(
            user=x,
            email_verification_status=UserEnhancement.EMAIL_VERIFICATION_COMPLETED
        )

    @override_settings(
        DAE_ADMIN_SIGNUP_NOTIFICATION=(
            ('django', 'django@localhost', ('mail', )),
            ('foo', 'foo@localhost', ('mail', )),
        )
    )
    def test_all_valid(self):
        """Should print a success message to stdout."""

        call_command('authenhanced', 'admin-notification', stdout=self.out)
        self.assertIn('[ok] Notification settings are valid!', self.out.getvalue())

    @override_settings(
        DAE_ADMIN_SIGNUP_NOTIFICATION=(
            ('django', 'django@localhost', ('mail', )),
            ('foo', 'foo@localhost', ('mail', )),
            ('bar', 'bar@localhost', ('mail', )),
        )
    )
    def test_address_unverified(self):
        """One of the accounts has an unverified email address."""

        with self.assertRaisesMessage(
            CommandError,
            "The following accounts do not have a verified email address: bar. "
            "Administrative notifications will only be sent to verfified email "
            "addresses."
        ):
            call_command('authenhanced', 'admin-notification', stdout=self.out)

    @override_settings(
        DAE_ADMIN_SIGNUP_NOTIFICATION=(
            ('django', 'django@localhost', ('mail', )),
            ('foo', 'foo@localhost', ('mail', )),
            ('baz', 'baz@localhost', ('mail', )),
        )
    )
    def test_insufficient_permissions(self):
        """One of the accounts does not have sufficient permissions."""

        with self.assertRaisesMessage(
            CommandError,
            "The following accounts do not have the sufficient permissions to "
            "actually modify accounts: baz."
        ):
            call_command('authenhanced', 'admin-notification', stdout=self.out)


@tag('command')
class CheckEmailUniquenessTests(AuthEnhancedTestCase):
    """These tests target the 'check_email_uniqueness()'-function.

    See auth_enhanced/management/commands/_lib.py"""

    def test_all_addresses_unique(self):
        """Should print a success message to stdout."""

        # prepare test environment to capture stdout
        out = StringIO()

        user_model = get_user_model()

        # create two users
        u = user_model.objects.create_user(**{          # noqa
            user_model.USERNAME_FIELD: 'django',        # noqa
            user_model.EMAIL_FIELD: 'django@localhost'  # noqa
        })                                              # noqa
        v = user_model.objects.create_user(**{          # noqa
            user_model.USERNAME_FIELD: 'foo',           # noqa
            user_model.EMAIL_FIELD: 'foo@localhost'     # noqa
        })                                              # noqa

        call_command('authenhanced', 'unique-email', stdout=out)
        self.assertIn('[ok] All email addresses are unique!', out.getvalue())

    def test_addresses_not_unique(self):
        """Should print a success message to stdout."""

        # prepare test environment to capture stdout
        out = StringIO()

        user_model = get_user_model()

        # create two users
        u = user_model.objects.create_user(**{          # noqa
            user_model.USERNAME_FIELD: 'django',        # noqa
            user_model.EMAIL_FIELD: 'django@localhost'  # noqa
        })                                              # noqa
        v = user_model.objects.create_user(**{          # noqa
            user_model.USERNAME_FIELD: 'foo',           # noqa
            user_model.EMAIL_FIELD: 'django@localhost'  # noqa
        })                                              # noqa

        with self.assertRaisesMessage(
            CommandError,
            "The following accounts don't have unique email addresses: django, foo"
        ):
            call_command('authenhanced', 'unique-email', stdout=out)
