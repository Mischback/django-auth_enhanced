# -*- coding: utf-8 -*-
"""This file contains the actual implementation of the commands."""

# Django imports
from django.contrib.auth import get_user_model
from django.core.management.base import CommandError
from django.db.models import Count


def check_admin_notification(stdout):
    """Checks, if the respective setting contains valid accounts with verified
    email addresses."""
    stdout.write('[.] check_admin_notification()')


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
