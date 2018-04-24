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
    @override_settings(DAE_OPERATION_MODE='DAE_CONST_MODE_AUTO_ACTIVATION')
    def test_exclude_email_field_1(self):
        """The email field should be removed, if it is not required.

        See '__init__()'-method."""

        form = SignupForm()
        self.assertNotIn(get_user_model().EMAIL_FIELD, form.fields)

    @tag('settings', 'setting_operation_mode')
    @override_settings(DAE_OPERATION_MODE='DAE_CONST_MODE_MANUAL_ACTIVATION')
    def test_exclude_email_field_2(self):
        """The email field should be removed, if it is not required.

        See '__init__()'-method."""

        form = SignupForm()
        self.assertNotIn(get_user_model().EMAIL_FIELD, form.fields)

    @tag('settings', 'setting_operation_mode')
    @override_settings(DAE_OPERATION_MODE='DAE_CONST_MODE_EMAIL_ACTIVATION')
    def test_include_email_field(self):
        """The email field should be included, if it is required.

        See '__init__()'-method."""

        form = SignupForm()
        self.assertIn(get_user_model().EMAIL_FIELD, form.fields)

    @tag('settings', 'setting_operation_mode')
    @override_settings(DAE_OPERATION_MODE='DAE_CONST_MODE_EMAIL_ACTIVATION')
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
    @override_settings(DAE_OPERATION_MODE='DAE_CONST_MODE_EMAIL_ACTIVATION')
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
    @override_settings(DAE_OPERATION_MODE='DAE_CONST_MODE_EMAIL_ACTIVATION')
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
    @override_settings(DAE_OPERATION_MODE='DAE_CONST_MODE_EMAIL_ACTIVATION')
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
    @override_settings(DAE_OPERATION_MODE='DAE_CONST_MODE_EMAIL_ACTIVATION')
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

    @override_settings(DAE_OPERATION_MODE='DAE_CONST_MODE_AUTO_ACTIVATION')
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
    @override_settings(DAE_OPERATION_MODE='DAE_CONST_MODE_AUTO_ACTIVATION')
    def test_save_is_active_auto_true(self):
        """If 'DAE_OPERATION_MODE' is set to automatic activation, the user
        object is created with 'is_active' = False.

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
    @override_settings(DAE_OPERATION_MODE='DAE_CONST_MODE_MANUAL_ACTIVATION')
    def test_save_is_active_auto_false(self):
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
