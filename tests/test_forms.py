# -*- coding: utf-8 -*-
"""Includes tests targeting the app-specific forms.

    - target file: auth_enhanced/forms.py
    - included tags: 'forms', 'settings', 'setting_operation_mode', 'signup'

The app's checks rely on Django's system check framework."""

# Python imports
from unittest import skip  # noqa

# Django imports
from django.contrib.auth import get_user_model
from django.forms import ValidationError
from django.test import override_settings, tag  # noqa

# app imports
from auth_enhanced.forms import SignupForm

# app imports
from .utils.testcases import AuthEnhancedTestCase


@tag('forms', 'signup')
class SignupFormTests(AuthEnhancedTestCase):
    """These tests target the SignupForm.

    SignupForm is derived from Django's 'UserCreationForm' and adds some small
    additional functions.

    TODO: Cache 'get_user_model()' in class variable or something..."""

    @tag('settings', 'setting_operation_mode')
    @override_settings(DAE_OPERATION_MODE='DAE_MODE_AUTO_ACTIVATION')
    def test_exclude_email_field_1(self):
        """The email field should be removed, if it is not required.

        See '__init__()'-method."""

        form = SignupForm()
        self.assertNotIn(get_user_model().EMAIL_FIELD, form.fields)

    @tag('settings', 'setting_operation_mode')
    @override_settings(DAE_OPERATION_MODE='DAE_MODE_MANUAL_ACTIVATION')
    def test_exclude_email_field_2(self):
        """The email field should be removed, if it is not required.

        See '__init__()'-method."""

        form = SignupForm()
        self.assertNotIn(get_user_model().EMAIL_FIELD, form.fields)

    @tag('settings', 'setting_operation_mode')
    @override_settings(DAE_OPERATION_MODE='DAE_MODE_EMAIL_ACTIVATION')
    def test_include_email_field(self):
        """The email field should be included, if it is required.

        See '__init__()'-method."""

        form = SignupForm()
        self.assertIn(get_user_model().EMAIL_FIELD, form.fields)

    @tag('settings', 'setting_operation_mode')
    @override_settings(DAE_OPERATION_MODE='DAE_MODE_EMAIL_ACTIVATION')
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
    @override_settings(DAE_OPERATION_MODE='DAE_MODE_EMAIL_ACTIVATION')
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
    @override_settings(DAE_OPERATION_MODE='DAE_MODE_EMAIL_ACTIVATION')
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
    @override_settings(DAE_OPERATION_MODE='DAE_MODE_EMAIL_ACTIVATION')
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
    @override_settings(DAE_OPERATION_MODE='DAE_MODE_EMAIL_ACTIVATION')
    def test_unique_email(self):
        """An email address must not be registered twice!

        See 'clean()'-method."""

        user = get_user_model().objects.create(**{
            get_user_model().USERNAME_FIELD: 'django',
            get_user_model().EMAIL_FIELD: 'foo@localhost'
        })

        form = SignupForm(
            data={
                get_user_model().USERNAME_FIELD: 'foo',
                'password1': 'foo',
                'password2': 'foo',
                get_user_model().EMAIL_FIELD: 'foo@localhost'
            }
        )
        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(ValidationError, 'This email address is already in use! Email addresses may only be registered once!')
