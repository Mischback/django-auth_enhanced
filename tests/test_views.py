# -*- coding: utf-8 -*-
"""Includes tests targeting the app's views.

    - target file: auth_enhanced/views.py
    - included tags: 'verification', 'views'"""


# Python imports
from unittest import skip  # noqa

# Django imports
from django.contrib.auth import get_user_model
from django.test import RequestFactory, override_settings, tag  # noqa

# app imports
from auth_enhanced.exceptions import AuthEnhancedException
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

        @staticmethod
        def is_valid_true(mock_obj):
            return True

        @staticmethod
        def is_valid_false(mock_obj):
            return False

        @staticmethod
        def raise_something(mock_obj):
            raise AuthEnhancedException('bar')

    @mock.patch('auth_enhanced.forms.EmailVerificationForm.activate_user')
    def test_form_valid_ok(self, mock_func):
        """Calling 'form_valid()' should activate the user by using the form's
        method 'activate_user'."""

        view = setup_view(
            EmailVerificationView(),
            RequestFactory().get('/foo/')
        )

        view.form_valid(view.get_form())

        self.assertTrue(mock_func.called)

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

    @mock.patch('auth_enhanced.forms.EmailVerificationForm.is_valid', MockEmailVerificationForm.is_valid_true)
    @mock.patch('auth_enhanced.views.EmailVerificationView.form_valid')
    def test_get_verification_token_valid(self, mock_func):
        """Call the view with a token in the url should verify the token."""

        view = setup_view(
            EmailVerificationView(),
            RequestFactory().get('/foo/')
        )

        view.get(
            RequestFactory().get('/foo/'),
            verification_token='foo'
        )

        self.assertTrue(mock_func.called)

    @mock.patch('auth_enhanced.forms.EmailVerificationForm.is_valid', MockEmailVerificationForm.is_valid_false)
    @mock.patch('auth_enhanced.views.redirect', MockEmailVerificationForm.raise_something)
    def test_get_verification_token_invalid(self):
        """Call the view with a token in the url should verify the token.

        Please notice the mock of 'redirect'. The method is mocked in its
        imported context (in 'auth_enhanced.views')."""

        view = setup_view(
            EmailVerificationView(),
            RequestFactory().get('/foo/')
        )

        with self.assertRaises(AuthEnhancedException):
            retval = view.get(                  # noqa
                RequestFactory().get('/foo/'),  # noqa
                verification_token='foo'        # noqa
            )                                   # noqa

    @mock.patch('django.views.generic.edit.ProcessFormView.get')
    def test_get_plain(self, mock_func):
        """Call the view without a token."""

        view = setup_view(
            EmailVerificationView(),
            RequestFactory().get('/foo/')
        )

        view.get(RequestFactory().get('/foo/'))

        self.assertTrue(mock_func)
