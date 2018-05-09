# -*- coding: utf-8 -*-
"""Provides the 'authenhanced' management command, that is used to control and
check certain bits of 'django-auth_ehanced'."""

# Django imports
from django.core.management.base import BaseCommand, CommandError

# app imports
from auth_enhanced.management.commands._lib import check_email_uniqueness


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

        # self.stdout.write('[!] found command {}'.format(options['cmd']))
        self.cmd = options['cmd'][0]

        if 'unique-email' == self.cmd:
            check_email_uniqueness(self.stdout)
        elif 'admin-notification' == self.cmd:
            self.stdout.write('[.] checking the admin notification setting')
        elif 'full' == self.cmd:
            self.stdout.write('[.] performing all app-specific check!')
        else:
            raise CommandError("No valid command was provided!")

    def get_version(self):
        """By overriding this method, the app can provide its own version."""
        return '0.1.0'
