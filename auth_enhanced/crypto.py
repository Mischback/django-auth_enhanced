# -*- coding: utf-8 -*-
"""Handles all crypto-related stuff of the app.

No, 'django-auth_enhanced' does *not* implement its own cryptographic
functions, classes or methods. It relies on Django's own security features.
This file provides some wrappers, to make the usage more conistent and
convenient."""

# Django imports
from django.conf import settings
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from django.utils.translation import ugettext_lazy as _

# app imports
from auth_enhanced.exceptions import AuthEnhancedException


class EnhancedCrypto(object):
    """A single interface to all of Django's crypto features.

    And as a side-note: I really like how this reads: *enhanced* crypto! (;"""

    def __init__(self):
        """Create the required instance of Signer."""

        # this parameter determines, how long a verification token is considered
        #   valid. Please be aware, that this setting is applied to all
        #   verification processes in the app.
        self.max_age = settings.DAE_VERIFICATION_TOKEN_MAX_AGE

        # get Django's signer with an app-specific salt (see settings.py for details)
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

    def verify_token(self, token=None):
        """Verifys a token by using Django's TimestampSigner.unsign().

        Returns the value, that has been signed to be re-used later."""

        try:
            val =  self.signer.unsign(token, max_age=self.max_age)
        # ok, the order of catching is relevant here...
        except SignatureExpired:
            raise
        except BadSignature:
            raise self.EnhancedCryptoException(
                _(
                    "Something went wrong during crypto operations. This error "
                    "message is unspecific to prevent any fingerprinting."
                )
            )
        except TypeError:
            raise self.EnhancedCryptoException(
                _(
                    "'verify_token()' was called without an actual token. "
                    "You see this message, because this is probably a "
                    "programming error/mistake."
                )
            )

        return val
