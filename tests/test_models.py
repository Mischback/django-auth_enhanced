# -*- coding: utf-8 -*-
"""Includes tests targeting the app-specific models.

    - target file: auth_enhanced/models.py
    - included tags: 'models', 'signals'"""

# Python imports
from unittest import skip  # noqa

# Django imports
from django.contrib.auth import get_user_model
from django.test import override_settings, tag  # noqa

# app imports
from auth_enhanced.models import UserEnhancement

# app imports
from .utils.testcases import (
    AuthEnhancedNoSignalsTestCase, AuthEnhancedTestCase,
)


@tag('models')
class UserEnhancementTests(AuthEnhancedTestCase):
    """Tests targeting the model class."""

    def test_email_is_verified(self):
        """Does the boolean abstraction work?

        See 'email_is_verified()'-method.

        This test actually relies on the applied 'post_save'-signal, registered
        in 'apps.py', meaning, that the 'UserEnhancement'-object is created
        automatically."""

        # create a User-object; post_save will create a UserEnhancement automatically
        u = get_user_model().objects.create(username='foo')

        # the UserEnhancement-object will be created with 'email_verification_status'
        #   set to 'EMAIL_VERIFICATION_FAILED', which should be evaluated as
        #   'False'
        self.assertEqual(u.enhancement.email_verification_status, UserEnhancement.EMAIL_VERIFICATION_FAILED)
        self.assertFalse(u.enhancement.email_is_verified)

        # manually update 'email_verification_status', but should still be
        #   considered 'False'
        u.enhancement.email_verification_status = UserEnhancement.EMAIL_VERIFICATION_IN_PROGRESS
        self.assertEqual(u.enhancement.email_verification_status, UserEnhancement.EMAIL_VERIFICATION_IN_PROGRESS)
        self.assertFalse(u.enhancement.email_is_verified)

        # another manual update, now it should evaluate to 'True'
        u.enhancement.email_verification_status = UserEnhancement.EMAIL_VERIFICATION_COMPLETED
        self.assertEqual(u.enhancement.email_verification_status, UserEnhancement.EMAIL_VERIFICATION_COMPLETED)
        self.assertTrue(u.enhancement.email_is_verified)


@tag('models', 'signals')
class UserEnhancementTestsDisabledSignalHandler(AuthEnhancedNoSignalsTestCase):

    def test_callback_create_enhancement_object_not_created(self):
        """If this is not a newly created object, do nothing.

        See 'callback_create_enhancement_object()'-method."""

        retval = UserEnhancement.callback_create_enhancement_object(
            get_user_model(),
            None,
            False,  # this is the relevant 'created' parameter!
        )
        self.assertIsNone(retval)

    def test_callback_create_enhancement_object_instance(self):
        """Django will pass the saved 'instance' along."""

        # create a User object to pass along
        u = get_user_model().objects.create(username='foo')

        retval = UserEnhancement.callback_create_enhancement_object(
            get_user_model(),
            u,
            True,
        )

        self.assertIsInstance(retval, UserEnhancement)
        self.assertEqual(retval.user, u)

    def test_callback_create_enhancement_object_obj(self):
        """The related object may be passed with 'user_obj'."""

        # create a User object to pass along
        u = get_user_model().objects.create(username='foo')

        retval = UserEnhancement.callback_create_enhancement_object(
            get_user_model(),
            None,
            True,
            user_obj=u
        )

        self.assertIsInstance(retval, UserEnhancement)
        self.assertEqual(retval.user, u)

    def test_callback_create_enhancement_object_id(self):
        """The related object may be passed by its 'user_id'."""

        # create a User object to pass along
        u = get_user_model().objects.create(username='foo')

        retval = UserEnhancement.callback_create_enhancement_object(
            get_user_model(),
            None,
            True,
            user_id=u.pk
        )

        self.assertIsInstance(retval, UserEnhancement)
        self.assertEqual(retval.user, u)

    def test_callback_create_enhancement_object_id_invalid(self):
        """Invalid 'user_id' will raise an exception."""

        with self.assertRaisesMessage(
            UserEnhancement.UserEnhancementException,
            'The given user id does not exist!'
        ):
            retval = UserEnhancement.callback_create_enhancement_object(    # noqa
                get_user_model(),                                           # noqa
                None,                                                       # noqa
                True,                                                       # noqa
                user_id=1337                                                # noqa
            )                                                               # noqa

    def test_callback_create_enhancement_object_no_param(self):
        """Invalid 'user_id' will raise an exception."""

        with self.assertRaisesMessage(
            UserEnhancement.UserEnhancementException,
            'Could not determine a valid user object!'
        ):
            retval = UserEnhancement.callback_create_enhancement_object(    # noqa
                get_user_model(),                                           # noqa
                None,                                                       # noqa
                True,                                                       # noqa
            )                                                               # noqa
