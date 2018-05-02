# -*- coding: utf-8 -*-
"""Includes tests targeting the app's views.

    - target file: auth_enhanced/views.py
    - included tags: 'verification', 'views'"""


# Python imports
from unittest import skip  # noqa

# Django imports
from django.contrib.auth import get_user_model
from django.test import override_settings, RequestFactory, tag  # noqa

# app imports
from auth_enhanced.forms import EmailVerificationForm
from auth_enhanced.views import EmailVerificationView

# app imports
from .utils.testcases import AuthEnhancedTestCase

try:
    from unittest import mock
except ImportError:
    import mock


def setup_view(view, request, *args, **kwargs):
    """Mimic ``as_view()``, but returns view instance.
    Use this function to get view instances on which you can run unit tests,
    by testing specific methods.

    See https://stackoverflow.com/a/33647251 and
    http://django-downloadview.readthedocs.io/en/latest/testing.html#django_downloadview.test.setup_view"""

    view.request = request
    view.args = args
    view.kwargs = kwargs

    return view


@tag('views', 'verification')
class EmailVerificationViewTests(AuthEnhancedTestCase):
    """These tests target the 'EmailVerificationView'"""

    class MockEmailVerificationForm(EmailVerificationForm):
        """This class just provides necessary mock methods."""

        @staticmethod
        def activate_user_does_not_exist(mock_obj):
            raise get_user_model().DoesNotExist('bar')

    @mock.patch('auth_enhanced.forms.EmailVerificationForm.activate_user')
    def test_form_valid_ok(self, mock):
        """Calling 'form_valid()' should activate the user by using the form's
        method 'activate_user'."""

        view = setup_view(
            EmailVerificationView(),
            RequestFactory().get('/foo/')
        )

        view.form_valid(view.get_form())

        self.assertTrue(mock.called)

    @mock.patch(
        'auth_enhanced.forms.EmailVerificationForm.activate_user',
        MockEmailVerificationForm.activate_user_does_not_exist
    )
    def test_form_valid_exception(self):
        """Even if the form is valid, the user object is checked, which may
        fail. Check if the exception is handled."""

        view = setup_view(
            EmailVerificationView(),
            RequestFactory().get('/foo/')
        )
        with self.assertRaises(get_user_model().DoesNotExist):
            view.form_valid(view.get_form())
