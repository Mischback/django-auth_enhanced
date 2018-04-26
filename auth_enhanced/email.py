# -*- coding: utf-8 -*-
"""Handles all email-related stuff of the app."""


# Django imports
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

# app imports
from auth_enhanced.exceptions import AuthEnhancedException
from auth_enhanced.settings import (
    DAE_CONST_MODE_AUTO_ACTIVATION, DAE_CONST_MODE_EMAIL_ACTIVATION,
    DAE_CONST_MODE_MANUAL_ACTIVATION,
)


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
            self.body = txt_body.strip()
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


def callback_admin_information_new_signup(sender, instance, created, **kwargs):
    """Sends an email to specified admins to inform them of a new signup.

    This function acts like a callback to a 'post_save'-signal."""

    # only send email on new registration
    if created:

        # set the email subject
        mail_subject = 'New Signup Notification'
        if settings.DAE_EMAIL_ADMIN_NOTIFICATION_PREFIX:
            mail_subject = '[{}] {}'.format(settings.DAE_EMAIL_ADMIN_NOTIFICATION_PREFIX, mail_subject)

        # prepare the recipient list
        mail_to = [(x[0], x[1]) for x in settings.DAE_ADMIN_SIGNUP_NOTIFICATION if 'mail' in x[2]]

        # TODO: prepare the context
        mail_context = {
            'admin_link_url': '{}://{}'.format(
                settings.DAE_EMAIL_ADMIN_LINK_SCHEME,
                settings.DAE_EMAIL_ADMIN_LNK_AUTHORITY
            ),
            'new_user': instance,
            'project_home': settings.DAE_EMAIL_HOME_VIEW_NAME,
            'project_link_url': '{}://{}'.format(
                settings.DAE_EMAIL_LINK_SCHEME,
                settings.DAE_EMAIL_LINK_AUTHORITY
            ),
            'project_name': settings.DAE_PROJECT_NAME,
            'user_model': get_user_model()._meta,
            'webmaster_email': settings.DAE_EMAIL_FROM_ADDRESS,
        }

        if settings.DAE_OPERATION_MODE == DAE_CONST_MODE_AUTO_ACTIVATION:
            mail_context['mode_auto'] = True
        elif settings.DAE_OPERATION_MODE == DAE_CONST_MODE_EMAIL_ACTIVATION:
            mail_context['mode_email'] = True
        elif settings.DAE_OPERATION_MODE == DAE_CONST_MODE_MANUAL_ACTIVATION:
            mail_context['mode_manual'] = True

        # create the email objects
        mails = []
        for m in mail_to:
            # add the username to the context
            loop_mail_context = mail_context
            loop_mail_context['admin_name'] = m[0]

            mails.append(
                AuthEnhancedEmail(
                    template_name='admin_signup_notification',
                    context=loop_mail_context,
                    subject=mail_subject,
                    from_email=settings.DAE_EMAIL_FROM_ADDRESS,
                    to=(m[1], )
                )
            )

        # get an email connection
        connection = get_connection()
        connection.send_messages(mails)
