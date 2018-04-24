# -*- coding: utf-8 -*-
"""Handles all email-related stuff of the app."""


# Django imports
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

# app imports
from auth_enhanced.exceptions import AuthEnhancedException


class AuthEnhancedEmail(EmailMultiAlternatives):
    """Base class for all app-related email messages."""

    def __init__(self, txt_template=None, html_template=None, context=None, **kwargs):

        # remove the body, because the app relies on templates instead
        try:
            del kwargs['body']
        except KeyError:
            # 'body' was not specified, so we just 'pass'
            pass

        # call the parent constructor
        super(AuthEnhancedEmail, self).__init__(**kwargs)

        # check for 'txt_template'
        # TODO: Is this really a minimum requirement?
        if not txt_template:
            raise self.AuthEnhancedEmailException(_("A 'txt_template' must be provided!"))

        # check for context (required for rendering)
        # TODO: Can this be handled more graceful? I.e by defaulting 'context' to {}?
        if context is None or not isinstance(context, dict):
            raise self.AuthEnhancedEmailException(_("A 'context' must be provided!"))

        # render and attach the 'txt_body'
        txt_body = render_to_string('{}/{}'.format(settings.DAE_EMAIL_TEMPLATE_PREFIX, txt_template), context)
        self.body = txt_body

        # render an alternative 'html_body'
        if html_template:
            html_body = render_to_string('{}/{}'.format(settings.DAE_EMAIL_TEMPLATE_PREFIX, html_template), context)
            self.attach_alternative(html_body, 'text/html')

    class AuthEnhancedEmailException(AuthEnhancedException):
        """This exception indicates, that something went wrong inside the class."""
        pass
