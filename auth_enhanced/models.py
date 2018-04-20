# -*- coding: utf-8 -*-
"""Contains app-specific models.

'django-auth_enhanced' relies heavily on Django's 'auth' app. One of the
guiding principles of 'django-auth_enhanced' was to reuse Django's default
User model. However, for some functions additional information has to be
stored.

Though Django's 'auth' app was focused, 'django-auth_enhanced' tries to be as
pluggable as possible."""


# Django imports
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserEnhancement(models.Model):
    """This class stores all necessary additional data on Django's User objects.

    Please note, that this model is meant to be pluggable by using a reference
    to 'AUTH_USER_MODEL'."""

    EMAIL_VERIFICATION_COMPLETED = 'EMAIL_VERIFICATION_COMPLETED'
    EMAIL_VERIFICATION_IN_PROGRESS = 'EMAIL_VERIFICATION_IN_PROGRESS'
    EMAIL_VERIFICATION_FAILED = 'EMAIL_VERIFICATION_FAILED'
    EMAIL_VERIFICATION_STATUS = (
        (EMAIL_VERIFICATION_COMPLETED, _("")),
        (EMAIL_VERIFICATION_IN_PROGRESS, _("")),
        (EMAIL_VERIFICATION_FAILED, _(""))
    )

    # the actual verification status
    email_verification_status = models.CharField(
        max_length=30,
        choices=EMAIL_VERIFICATION_STATUS,
        default=EMAIL_VERIFICATION_FAILED,
    )

    # a reference to the user object
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    @property
    def email_is_verified(self):
        """Returns a simple boolean value, depending on the 'email_verification_status'"""

        if self.email_verification_status == self.EMAIL_VERIFICATION_COMPLETED:
            return True

        return False
