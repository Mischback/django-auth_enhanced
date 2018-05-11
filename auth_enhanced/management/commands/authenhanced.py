# -*- coding: utf-8 -*-
"""Provides the 'authenhanced' management command, that is used to control and
check certain bits of 'django-auth_ehanced'."""

# Django imports
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count

# app imports
from auth_enhanced.models import UserEnhancement


def check_admin_notification():
    """Checks, if the respective setting contains valid accounts with verified
    email addresses."""

    user_model = get_user_model()

    # extract the list of usernames
    username_list = [x[0] for x in settings.DAE_ADMIN_SIGNUP_NOTIFICATION]

    # check, if all listed accounts have verified email addresses
    verified_email = (
        # get listed accounts
        user_model.objects.filter(
            # this really complex statement is used, to not reference the
            #   'username' field directly, to be as pluggable as possible
            **{'{}__in'.format(user_model.USERNAME_FIELD): username_list}
        )
        # this filter only delivers accounts with verified email addresses
        .filter(enhancement__email_verification_status=UserEnhancement.EMAIL_VERIFICATION_COMPLETED)
    )

    # determine, which accounts do have unverified email addresses
    if len(username_list) > len(verified_email):
        # actually build the list to raise the error message
        unverified_email = [
            u for u in username_list if u not in verified_email.values_list(
                user_model.USERNAME_FIELD, flat=True
            )
        ]

        # TODO: For the moment, this is perfectly fine. But if there are some
        #   more, different notification methods, this might not be necessary
        #   anymore. This check then have to take the specified 'notification-
        #   method' into consideration. Instead of raising the CommandError,
        #   only a warning has to be displayed.
        raise CommandError(
            "The following accounts do not have a verified email address: {}. "
            "Administrative notifications will only be sent to verfified email "
            "addresses.".format(', '.join(unverified_email))
        )

    # determine, if the specified users have sufficient permissions
    # TODO: For the moment, only superusers are able to actually change
    #   user-objects. If there is a custom permission system, it is possible
    #   to actually check for more specific conditions/permissions
    authorised_users = verified_email.filter(is_superuser=True)

    if len(username_list) > len(authorised_users):
        unauthorised_users = [
            u for u in username_list if u not in authorised_users.values_list(
                user_model.USERNAME_FIELD, flat=True
            )
        ]

        raise CommandError(
            "The following accounts do not have the sufficient permissions to "
            "actually modify accounts: {}.".format(', '.join(unauthorised_users))
        )

    return True


def check_email_uniqueness():
    """This function checks, if all email addresses are unique."""

    user_model = get_user_model()

    # find the email addresses, that are not unique
    non_unique_emails = (
        # get all email addresses
        user_model.objects.values(user_model.EMAIL_FIELD)
        # annotate them by counting a guaranteed unique field
        .annotate(count=Count('pk'))
        # get all email addresses, that appear more than one time
        .filter(count__gt=1)
        # remove the annotation again
        .values(user_model.EMAIL_FIELD)
    )

    if non_unique_emails:
        # get the usernames of accounts, that have non-unique email addresses
        non_unique_accounts = (
            user_model.objects.filter(
                # this really complex statement is used, to not reference the
                #   'email' field directly, to be as pluggable as possible
                **{'{}__in'.format(user_model.EMAIL_FIELD): non_unique_emails}
            )
            # simply list the usernames
            .values_list(user_model.USERNAME_FIELD, flat=True)
        )

        # raise an Error and include a list of usernames without unique email
        #   addresses
        raise CommandError(
            "The following accounts don't have unique email addresses: {}".format(
                ', '.join(non_unique_accounts)
            )
        )

    return True


class Command(BaseCommand):
    """Provides the command 'authenhanced'."""

    help = (
        "This is an app-specific Django management command, that is used to "
        "enhance and support django-auth_enhanced's functions."
    )

    def add_arguments(self, parser):
        """These arguments will be recognized by this command."""

        parser.add_argument(
            'cmd', nargs=1,
            help=(
                "The actual command to perform (accepted values: "
                "'admin-notification', "
                "'unique-email', "
                "and 'full')"
            )
        )

    def handle(self, *args, **options):
        """Check, which of the available commands is to be executed."""

        self.cmd = options['cmd'][0]

        if self.cmd not in ('unique-email', 'admin-notification', 'full'):
            raise CommandError("No valid command was provided!")

        if self.cmd in ('unique-email', 'full'):
            if check_email_uniqueness():
                # all email addresses are unique!
                self.stdout.write(
                    self.style.SUCCESS('[ok] All email addresses are unique!')
                )

        if self.cmd in ('admin-notification', 'full'):
            if check_admin_notification():
                self.stdout.write(
                    self.style.SUCCESS('[ok] Notification settings are valid!')
                )

    def get_version(self):
        """By overriding this method, the app can provide its own version."""
        return '0.1.0'
