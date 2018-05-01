# -*- coding: utf-8 -*-
"""Handles all crypto-related stuff of the app.

No, 'django-auth_enhanced' does *not* implement its own cryptographic
functions, classes or methods. It relies on Django's own security features.
This file provides some wrappers, to make the usage more conistent and
convenient."""

# Django imports
from django.conf import settings
from django.core.signing import TimestampSigner
from django.utils.translation import ugettext_lazy as _

# app imports
from auth_enhanced.exceptions import AuthEnhancedException


class EnhancedCrypto(object):
    """A single interface to all of Django's crypto features."""

    def __init__(self):
        """Create the required instance of Signer."""
        self.signer = TimestampSigner(salt=settings.DAE_SALT)

    class EnhancedCryptoException(AuthEnhancedException):
        """This Exception indicates, that something went wrong during crypto
        operations."""
        pass

    def get_verification_token(self, user_obj=None):
        """Returns a verification token by hashing the username."""

        try:
            token = self.signer.sign(getattr(user_obj, user_obj.USERNAME_FIELD))
        except AttributeError:
            raise self.EnhancedCryptoException(
                _(
                    "Something went wrong during crypto operations. This error "
                    "message is unspecific to prevent any fingerprinting."
                )
            )

        return token
