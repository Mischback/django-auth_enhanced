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
from .utils.testcases import AuthEnhancedTestCase

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


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
