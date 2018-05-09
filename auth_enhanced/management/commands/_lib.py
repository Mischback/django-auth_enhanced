# -*- coding: utf-8 -*-
"""This file contains the actual implementation of the commands."""

# Django imports
from django.contrib.auth import get_user_model
from django.core.management.base import CommandError
from django.db.models import Count


def check_email_uniqueness(stdout):
    """This function checks, if all email addresses are unique."""

    # find the email addresses, that are not unique
    non_unique_mails = (
        get_user_model().objects.values('email')
        .annotate(count=Count('id'))
        .filter(count__gt=1)
        .values('email')
    )

    if not non_unique_mails:
        # all email addresses are unique!
        stdout.write('[ok] All email addresses are unique!')
    else:

        # get the usernames of accounts, that have non-unique email addresses
        non_unique_accounts = (
            get_user_model().objects.filter(email__in=non_unique_mails)
            .values_list('username', flat=True)
        )

        # raise an Error and include a list of usernames without unique email
        #   addresses
        raise CommandError(
            "The following accounts don't have unique email addresses: {}".format(
                ', '.join(non_unique_accounts)
            )
        )
