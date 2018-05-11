# -*- coding: utf-8 -*-
"""Provides the 'authenhanced' management command, that is used to control and
check certain bits of 'django-auth_ehanced'."""

# Django imports
from django.core.management.base import BaseCommand, CommandError

# app imports
from auth_enhanced.management.commands._lib import (
    check_admin_notification, check_email_uniqueness,
)


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
