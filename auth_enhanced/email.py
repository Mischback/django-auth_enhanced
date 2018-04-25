# -*- coding: utf-8 -*-
"""Handles all email-related stuff of the app."""


# Django imports
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

# app imports
from auth_enhanced.exceptions import AuthEnhancedException


class AuthEnhancedEmail(EmailMultiAlternatives):
    """Base class for all app-related email messages."""

    def __init__(self, template_name=None, context=None, **kwargs):

        # remove the body, because the app relies on templates instead
        try:
            del kwargs['body']
        except KeyError:
            # 'body' was not specified, so we just 'pass'
            pass

        # call the parent constructor
        super(AuthEnhancedEmail, self).__init__(**kwargs)

        # check for 'template_name'
        # TODO: Is this really a minimum requirement?
        if not template_name:
            raise self.AuthEnhancedEmailException(_("A 'template_name' must be provided!"))

        # check for context (required for rendering)
        if context is None or not isinstance(context, dict):
            context = {}

        # render and attach the 'txt_body'
        try:
            txt_template = '{}/{}.txt'.format(settings.DAE_EMAIL_TEMPLATE_PREFIX, template_name)
            txt_body = render_to_string(txt_template, context)
            self.body = txt_body
        except TemplateDoesNotExist:
            # do stuff here!
            raise self.AuthEnhancedEmailException(_("You have to provide a text template '{}'.".format(txt_template)))

        # render an alternative 'html_body'
        try:
            html_template = '{}/{}.html'.format(settings.DAE_EMAIL_TEMPLATE_PREFIX, template_name)
            html_body = render_to_string(html_template, context)
            self.attach_alternative(html_body, 'text/html')
        except TemplateDoesNotExist:
            # no html-template is provided/present... Just skip this
            pass

    class AuthEnhancedEmailException(AuthEnhancedException):
        """This exception indicates, that something went wrong inside the class."""
        pass


def admin_information_new_signup(sender, instance, created, **kwargs):
    """Sends an email to specified admins to inform them of a new signup.

    This function acts like a callback to a 'post_save'-signal."""

    print('[!] sending mail to admins...')
