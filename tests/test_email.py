# -*- coding: utf-8 -*-
"""Includes tests targeting the email abstraction layer.

    - target file: auth_enhanced/email.py
    - included tags: 'email'"""

# Python imports
from unittest import skip  # noqa

# Django imports
from django.test import override_settings, tag  # noqa

# app imports
from auth_enhanced.email import AuthEnhancedEmail

# app imports
from .utils.testcases import AuthEnhancedTestCase


@tag('email')
class AuthEnhancedEmailTests(AuthEnhancedTestCase):
    """These tests target the base class for app-specific email objects."""

    def test_init_txt_template_required(self):
        """'txt_template' has to be given.

        See '__init__()'-method."""

        with self.assertRaisesMessage(
            AuthEnhancedEmail.AuthEnhancedEmailException,
            "A 'txt_template' must be provided!"
        ):
            mail = AuthEnhancedEmail()  # noqa

    def test_init_context_not_none(self):
        """'context' must not be None.

        See '__init__()'-method."""

        with self.assertRaisesMessage(
            AuthEnhancedEmail.AuthEnhancedEmailException,
            "A 'context' must be provided!"
        ):
            mail = AuthEnhancedEmail(txt_template='test.txt')  # noqa

    def test_init_context_not_dict(self):
        """'context' must be a 'dict'.

        See '__init__()'-method."""

        with self.assertRaisesMessage(
            AuthEnhancedEmail.AuthEnhancedEmailException,
            "A 'context' must be provided!"
        ):
            mail = AuthEnhancedEmail(txt_template='test.txt', context='foo')  # noqa

    @override_settings(DAE_EMAIL_TEMPLATE_PREFIX='mail')
    def test_init_render_txt(self):
        """Plain text should be rendered into 'body'-attribute.

        See '__init__()'-method."""

        mail = AuthEnhancedEmail(txt_template='test.txt', context={})
        self.assertIn('A Test Template for Emails', mail.body)

    @override_settings(DAE_EMAIL_TEMPLATE_PREFIX='mail')
    def test_init_render_html(self):
        """HTML text should be rendered into 'alternatives'-list.

        See '__init__()'-method."""

        mail = AuthEnhancedEmail(txt_template='test.txt', html_template='test.html', context={})
        # TODO: this seems really too 'hackish'...
        self.assertIn('A Test Template for Emails', mail.alternatives[0][0])
