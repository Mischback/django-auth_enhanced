# -*- coding: utf-8 -*-
"""Includes tests targeting the email abstraction layer.

    - target file: auth_enhanced/email.py
    - included tags: 'email'"""

# Python imports
from unittest import skip  # noqa

# Django imports
from django.conf import settings
from django.test import override_settings, tag  # noqa

# app imports
from auth_enhanced.email import AuthEnhancedEmail

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
