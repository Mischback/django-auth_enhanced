# -*- coding: utf-8 -*-
"""Includes tests targeting the app-specific forms.

    - target file: auth_enhanced/forms.py
    - included tags: 'forms', 'settings', 'setting_operation_mode', 'signup',
        'verification'

The app's checks rely on Django's system check framework."""

# Python imports
from unittest import skip  # noqa

# Django imports
from django.contrib.auth import get_user_model
from django.core.signing import SignatureExpired
from django.forms import ValidationError
from django.test import override_settings, tag  # noqa

# app imports
from auth_enhanced.crypto import EnhancedCrypto
from auth_enhanced.forms import EmailVerificationForm, SignupForm
from auth_enhanced.models import UserEnhancement
from auth_enhanced.settings import (
    DAE_CONST_MODE_AUTO_ACTIVATION, DAE_CONST_MODE_EMAIL_ACTIVATION,
    DAE_CONST_MODE_MANUAL_ACTIVATION,
)

# app imports
from .utils.testcases import AuthEnhancedTestCase

try:
    # Python 3
    from unittest import mock
except ImportError:
    # Python 2.7
    import mock


@tag('forms', 'verification')
class EmailVerificationFormTests(AuthEnhancedTestCase):
    """These tests target the EmailVerificationForm."""

    class MockVerifyToken:
        """This class just provides necessary mock methods."""

        @staticmethod
        def verify_token_valid(mock_obj, token=None):
            return 'foo'

        @staticmethod
        def verify_token_expired(mock_obj, token=None):
            raise SignatureExpired('bar')

        @staticmethod
        def verify_token_error(mock_obj, token=None):
            raise EnhancedCrypto.EnhancedCryptoException('bar')

    @mock.patch('auth_enhanced.crypto.EnhancedCrypto.verify_token', new=MockVerifyToken.verify_token_valid)
    def test_clean_token_valid(self):
        """A valid token is simply returned and the 'username'-attribute populated.

        See 'clean_token()'-method."""

        form = EmailVerificationForm(
            data={
                'token': 'foo',
            }
        )

        form.is_valid()
        cleaned_token = form.clean_token()
        self.assertEqual(cleaned_token, 'foo')
        self.assertEqual(form.username, 'foo')

    @override_settings(DAE_VERIFICATION_TOKEN_MAX_AGE=5)
    @mock.patch('auth_enhanced.crypto.EnhancedCrypto.verify_token', new=MockVerifyToken.verify_token_expired)
    def test_clean_token_expired(self):
        """An expired token will state a clear 'ValidationError'.

        See 'clean_token()'-method."""

        form = EmailVerificationForm(
            data={
                'token': 'foo',
            }
        )

        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(
            ValidationError,
            "It seems like you have submitted a valid verification "
            "token, that is expired. Be aware, that verification "
            "tokens are considered valid for 5 seconds and must be "
            "used within that time period."
        )
        self.assertEqual(form.username, None)

    @mock.patch('auth_enhanced.crypto.EnhancedCrypto.verify_token', new=MockVerifyToken.verify_token_error)
    def test_clean_token_error(self):
        """A failing token will raise a 'ValidationError' without real information.

        See 'clean_token()'-method."""

        form = EmailVerificationForm(
            data={
                'token': 'foo',
            }
        )

        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(ValidationError, "Your submitted token could not be verified!")
        self.assertEqual(form.username, None)

    def test_activate_user_valid(self):
        """A valid user will get activated and its 'email_verification_status' updated.

        See 'activate_user()'-method.

        This implicitly tests a non-existent UserEnhancement."""

        u = get_user_model().objects.create(username='foo', is_active=False)

        form = EmailVerificationForm()
        form.username = u.username

        self.assertFalse(u.is_active)

        form.activate_user()

        self.assertTrue(get_user_model().objects.get(username='foo').is_active)
        self.assertEqual(u.enhancement.email_verification_status, UserEnhancement.EMAIL_VERIFICATION_COMPLETED)

    def test_activate_user_invalid_user(self):
        """A non-existent user can not be activated and raises an exception.

        See 'activate_user()'-method."""

        form = EmailVerificationForm()
        form.username = 'bar'   # this username does not exist

        with self.assertRaises(get_user_model().DoesNotExist):
            form.activate_user()


@tag('forms', 'signup')
class SignupFormTests(AuthEnhancedTestCase):
    """These tests target the SignupForm.

    SignupForm is derived from Django's 'UserCreationForm' and adds some small
    additional functions.

    TODO: Cache 'get_user_model()' in class variable or something..."""

    @tag('settings', 'setting_operation_mode')
    @override_settings(DAE_OPERATION_MODE=DAE_CONST_MODE_AUTO_ACTIVATION)
    def test_exclude_email_field_1(self):
        """The email field should be removed, if it is not required.

        See '__init__()'-method."""

        form = SignupForm()
        self.assertNotIn(get_user_model().EMAIL_FIELD, form.fields)

    @tag('settings', 'setting_operation_mode')
    @override_settings(DAE_OPERATION_MODE=DAE_CONST_MODE_MANUAL_ACTIVATION)
    def test_exclude_email_field_2(self):
        """The email field should be removed, if it is not required.

        See '__init__()'-method."""

        form = SignupForm()
        self.assertNotIn(get_user_model().EMAIL_FIELD, form.fields)

    @tag('settings', 'setting_operation_mode')
    @override_settings(DAE_OPERATION_MODE=DAE_CONST_MODE_EMAIL_ACTIVATION)
    def test_include_email_field(self):
        """The email field should be included, if it is required.

        See '__init__()'-method."""

        form = SignupForm()
        self.assertIn(get_user_model().EMAIL_FIELD, form.fields)

    @tag('settings', 'setting_operation_mode')
    @override_settings(DAE_OPERATION_MODE=DAE_CONST_MODE_EMAIL_ACTIVATION)
    def test_required_email_field_missing(self):
        """Enforce required email addresses.

        See 'clean()'-method."""

        form = SignupForm(
            data={
                get_user_model().USERNAME_FIELD: 'foo',
                'password1': 'foo',
                'password2': 'foo'
            }
        )
        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(ValidationError, 'A valid email address is required!')

    @tag('settings', 'setting_operation_mode')
    @override_settings(DAE_OPERATION_MODE=DAE_CONST_MODE_EMAIL_ACTIVATION)
    def test_required_email_field_empty(self):
        """Enforce required email addresses.

        See 'clean()'-method."""

        form = SignupForm(
            data={
                get_user_model().USERNAME_FIELD: 'foo',
                'password1': 'foo',
                'password2': 'foo',
                get_user_model().EMAIL_FIELD: ''
            }
        )
        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(ValidationError, 'A valid email address is required!')

    @tag('settings', 'setting_operation_mode')
    @override_settings(DAE_OPERATION_MODE=DAE_CONST_MODE_EMAIL_ACTIVATION)
    def test_required_email_field_invalid(self):
        """Enforce required email addresses.

        See 'clean()'-method."""

        form = SignupForm(
            data={
                get_user_model().USERNAME_FIELD: 'foo',
                'password1': 'foo',
                'password2': 'foo',
                get_user_model().EMAIL_FIELD: 'foo.localhost'
            }
        )
        self.assertFalse(form.is_valid())
        # I'm quite happy, that the following assert works, but I didn't really
        #   know why. The email-field-validator does something, that makes this
        #   app's code trigger. Not really relevant, but interesting!
        self.assertRaisesMessage(ValidationError, 'A valid email address is required!')

    @tag('settings', 'setting_operation_mode')
    @override_settings(DAE_OPERATION_MODE=DAE_CONST_MODE_EMAIL_ACTIVATION)
    def test_required_email_field_valid(self):
        """Enforce required email addresses.

        See 'clean()'-method."""

        form = SignupForm(
            data={
                get_user_model().USERNAME_FIELD: 'foo',
                'password1': 'foo',
                'password2': 'foo',
                get_user_model().EMAIL_FIELD: 'foo@localhost'
            }
        )
        self.assertTrue(form.is_valid())

    @tag('settings', 'setting_operation_mode')
    @override_settings(DAE_OPERATION_MODE=DAE_CONST_MODE_EMAIL_ACTIVATION)
    def test_unique_email(self):
        """An email address must not be registered twice!

        See 'clean()'-method."""

        user = get_user_model().objects.create(**{          # noqa
            get_user_model().USERNAME_FIELD: 'django',      # noqa
            get_user_model().EMAIL_FIELD: 'foo@localhost'   # noqa
        })                                                  # noqa

        form = SignupForm(
            data={
                get_user_model().USERNAME_FIELD: 'foo',
                'password1': 'foo',
                'password2': 'foo',
                get_user_model().EMAIL_FIELD: 'foo@localhost'
            }
        )
        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(
            ValidationError,
            'This email address is already in use! Email addresses may only be registered once!'
        )

    @override_settings(DAE_OPERATION_MODE=DAE_CONST_MODE_AUTO_ACTIVATION)
    def test_save_no_commit(self):
        """SignupForm's 'save()'-method may be called without commiting.

        See 'save()'-method.

        While an 'override_settings()' is used, it is not really needed here
        and shall only ensure, that the form can be created like below. That's
        the reason, why this test is not tagged."""

        form = SignupForm(
            data={
                get_user_model().USERNAME_FIELD: 'foo',
                'password1': 'foo',
                'password2': 'foo'
            }
        )
        self.assertTrue(form.is_valid())

        user = form.save(commit=False)  # noqa

        # it should not be possible to fetch the user from the DB
        with self.assertRaises(get_user_model().DoesNotExist):
            db_user = get_user_model().objects.get(**{      # noqa
                get_user_model().USERNAME_FIELD: 'foo',     # noqa
            })                                              # noqa

    @tag('settings', 'setting_operation_mode')
    @override_settings(DAE_OPERATION_MODE=DAE_CONST_MODE_AUTO_ACTIVATION)
    def test_save_is_active_auto_true(self):
        """If 'DAE_OPERATION_MODE' is set to automatic activation, the user
        object is created with 'is_active' = True.

        See 'save()'-method."""

        form = SignupForm(
            data={
                get_user_model().USERNAME_FIELD: 'foo',
                'password1': 'foo',
                'password2': 'foo'
            }
        )
        self.assertTrue(form.is_valid())

        user = form.save()
        self.assertTrue(user.is_active)

    @tag('settings', 'setting_operation_mode')
    @override_settings(DAE_OPERATION_MODE=DAE_CONST_MODE_MANUAL_ACTIVATION)
    def test_save_is_active_auto_false_manual(self):
        """Depending on the 'DAE_OPERATION_MODE'-setting the user object is
        created with 'is_active' = False.

        See 'save()'-method."""

        form = SignupForm(
            data={
                get_user_model().USERNAME_FIELD: 'foo',
                'password1': 'foo',
                'password2': 'foo'
            }
        )
        self.assertTrue(form.is_valid())

        user = form.save()
        self.assertFalse(user.is_active)

    @tag('settings', 'setting_operation_mode')
    @override_settings(DAE_OPERATION_MODE=DAE_CONST_MODE_EMAIL_ACTIVATION)
    def test_save_is_active_auto_false_email(self):
        """Depending on the 'DAE_OPERATION_MODE'-setting the user object is
        created with 'is_active' = False.

        See 'save()'-method."""

        form = SignupForm(
            data={
                get_user_model().USERNAME_FIELD: 'foo',
                get_user_model().EMAIL_FIELD: 'foo@localhost',
                'password1': 'foo',
                'password2': 'foo'
            }
        )
        self.assertTrue(form.is_valid())

        user = form.save()
        self.assertFalse(user.is_active)
