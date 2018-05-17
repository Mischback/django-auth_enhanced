# -*- coding: utf-8 -*-
"""Includes tests targeting the email abstraction layer.

    - target file: auth_enhanced/email.py
    - included tags: 'email'"""

# Python imports
from unittest import skip  # noqa

# Django imports
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import override_settings, tag  # noqa

# app imports
from auth_enhanced.email import (
    AuthEnhancedEmail, callback_admin_information_new_signup,
    callback_user_signup_email_verification,
)
from auth_enhanced.settings import (
    DAE_CONST_MODE_AUTO_ACTIVATION, DAE_CONST_MODE_EMAIL_ACTIVATION,
    DAE_CONST_MODE_MANUAL_ACTIVATION,
)

# app imports
from .utils.testcases import AuthEnhancedTestCase


@tag('email')
class AuthEnhancedEmailTests(AuthEnhancedTestCase):
    """These tests target the base class for app-specific email objects."""

    def test_init_template_name_required(self):
        """'template_name' has to be given.

        See '__init__()'-method."""

        with self.assertRaisesMessage(
            AuthEnhancedEmail.AuthEnhancedEmailException,
            "A 'template_name' must be provided!"
        ):
            mail = AuthEnhancedEmail()  # noqa

    @override_settings(DAE_EMAIL_TEMPLATE_PREFIX='mail')
    def test_init_render_txt_and_html(self):
        """Plain text should be rendered into 'body'-attribute.

        See '__init__()'-method."""

        mail = AuthEnhancedEmail(template_name='test')
        self.assertIn('A Test Template for Emails', mail.body)
        # TODO: this seems really too 'hackish'...
        self.assertIn('A Test Template for Emails', mail.alternatives[0][0])

    @override_settings(DAE_EMAIL_TEMPLATE_PREFIX='mail')
    def test_init_txt_template_does_not_exist(self):
        """'template_name' must specify an existent template file.

        See '__init__()'-method."""

        unavailable_template = 'does-not-exist'

        with self.assertRaisesMessage(
            AuthEnhancedEmail.AuthEnhancedEmailException,
            "You have to provide a text template '{}/{}.txt'.".format(
                settings.DAE_EMAIL_TEMPLATE_PREFIX,
                unavailable_template
            )
        ):
            mail = AuthEnhancedEmail(template_name=unavailable_template)  # noqa

    @override_settings(DAE_EMAIL_TEMPLATE_PREFIX='mail')
    def test_init_only_txt_template(self):
        """If 'template_name'.html does not exist, only render txt-template.

        See '__init__()'-method."""

        only_txt_template = 'test_only_txt'
        mail = AuthEnhancedEmail(template_name=only_txt_template)
        self.assertIn('A Test Template for Emails', mail.body)


@tag('email')
@override_settings(
    DAE_ADMIN_SIGNUP_NOTIFICATION=(('django', 'django@localhost', ('mail', )), ),
    DAE_EMAIL_ADMIN_NOTIFICATION_PREFIX='',
    DAE_OPERATION_MODE=DAE_CONST_MODE_AUTO_ACTIVATION
)
class AdminInformationNewSignupTests(AuthEnhancedTestCase):
    """These tests target the 'callback_admin_information_new_signup'-function."""

    def test_callback_not_created(self):
        """If this is not a newly created object, do nothing.

        See 'callback_admin_information_new_signup()'-function."""

        retval = callback_admin_information_new_signup(
            get_user_model(),
            None,
            False,  # this is the relevant 'created' parameter!
        )
        self.assertFalse(retval)

    @override_settings(DAE_EMAIL_ADMIN_NOTIFICATION_PREFIX='foo')
    def test_callback_subject_prefix(self):
        """Is the subject line modified?

        See 'callback_admin_information_new_signup()'-function."""

        # create a User object to pass along
        u = get_user_model().objects.create(username='foo')

        retval = callback_admin_information_new_signup(
            get_user_model(),
            u,
            True
        )
        self.assertTrue(retval)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, '[{}] New Signup Notification'.format(
            settings.DAE_EMAIL_ADMIN_NOTIFICATION_PREFIX
        ))

    @override_settings(DAE_ADMIN_SIGNUP_NOTIFICATION=False)
    def test_callback_notification_false(self):
        """Recipient list can not be prepared if DAE_ADMIN_SIGNUP_NOTIFICATION is False.

        See 'callback_admin_information_new_signup()'-function."""

        # create a User object to pass along
        u = get_user_model().objects.create(username='foo')

        retval = callback_admin_information_new_signup(
            get_user_model(),
            u,
            True
        )
        self.assertFalse(retval)

    @override_settings(DAE_OPERATION_MODE=DAE_CONST_MODE_AUTO_ACTIVATION)
    def test_callback_apply_mode_auto(self):
        """Is 'context['mode_auto']' set?

        See 'callback_admin_information_new_signup()'-function."""

        # create a User object to pass along
        u = get_user_model().objects.create(username='foo')

        retval = callback_admin_information_new_signup(
            get_user_model(),
            u,
            True
        )
        self.assertTrue(retval)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('uses a signup system that activates users automatically', mail.outbox[0].body)

    @override_settings(DAE_OPERATION_MODE=DAE_CONST_MODE_EMAIL_ACTIVATION)
    def test_callback_apply_mode_email(self):
        """Is 'context['mode_email']' set?

        See 'callback_admin_information_new_signup()'-function."""

        # create a User object to pass along
        u = get_user_model().objects.create(username='foo')

        retval = callback_admin_information_new_signup(
            get_user_model(),
            u,
            True
        )
        self.assertTrue(retval)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(
            'uses a signup system that requires new users to verify their email address before they get activated',
            mail.outbox[0].body
        )

    @override_settings(DAE_OPERATION_MODE=DAE_CONST_MODE_MANUAL_ACTIVATION)
    def test_callback_apply_mode_manual(self):
        """Is 'context['mode_manual']' set?

        See 'callback_admin_information_new_signup()'-function."""

        # create a User object to pass along
        u = get_user_model().objects.create(username='foo')

        retval = callback_admin_information_new_signup(
            get_user_model(),
            u,
            True
        )
        self.assertTrue(retval)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('uses a signup system that requires the manual activation of accounts', mail.outbox[0].body)

    @override_settings(DAE_OPERATION_MODE='foo')
    def test_callback_apply_mode_none(self):
        """With an invalid operation mode, no context is applied.

        See 'callback_admin_information_new_signup()'-function."""

        # create a User object to pass along
        u = get_user_model().objects.create(username='foo')

        retval = callback_admin_information_new_signup(
            get_user_model(),
            u,
            True
        )
        self.assertTrue(retval)
        self.assertEqual(len(mail.outbox), 1)
        self.assertNotIn('uses a signup system that activates users automatically', mail.outbox[0].body)
        self.assertNotIn(
            'uses a signup system that requires new users to verify their email address before they get activated',
            mail.outbox[0].body
        )
        self.assertNotIn('uses a signup system that requires the manual activation of accounts', mail.outbox[0].body)


@tag('email')
@override_settings(
    DAE_ADMIN_SIGNUP_NOTIFICATION=(('django', 'django@localhost', ('mail', )), ),
    DAE_EMAIL_PREFIX='',
    DAE_OPERATION_MODE=DAE_CONST_MODE_EMAIL_ACTIVATION
)
class UserSignupEmailVerificationTests(AuthEnhancedTestCase):
    """These tests target the 'callback_user_signup_email_verification'-function."""

    def test_callback_not_created(self):
        """If this is not a newly created object, do nothing.

        See 'callback_user_signup_email_verification()'-function."""

        retval = callback_user_signup_email_verification(
            get_user_model(),
            None,
            False,  # this is the relevant 'created' parameter!
        )
        self.assertFalse(retval)

    @override_settings(DAE_EMAIL_PREFIX='foo')
    def test_callback_subject_prefix(self):
        """Is the subject line modified?

        See 'callback_user_signup_email_verification()'-function."""

        # create a User object to pass along
        u = get_user_model().objects.create(username='foo', email='foo@localhost')

        retval = callback_user_signup_email_verification(
            get_user_model(),
            u,
            True
        )
        self.assertTrue(retval)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, '[{}] Email Verification Mail'.format(
            settings.DAE_EMAIL_PREFIX
        ))
