# -*- coding: utf-8 -*-
"""Includes tests targeting the crypto abstraction layer.

    - target file: auth_enhanced/crypto.py
    - included tags: 'crypto'"""


# Python imports
from unittest import skip  # noqa

# Django imports
from django.contrib.auth import get_user_model
from django.core.signing import BadSignature, SignatureExpired
from django.test import override_settings, tag  # noqa

# app imports
from auth_enhanced.crypto import EnhancedCrypto

# app imports
from .utils.testcases import AuthEnhancedTestCase

try:
    from unittest import mock
except ImportError:
    import mock


@tag('crypto')
class EnhancedCryptoTests(AuthEnhancedTestCase):
    """These tests target the EnhancedCrypto class."""

    class MockSignUnsign(object):
        """This class just provides necessary mock methods."""

        @staticmethod
        def sign(mock_obj, item):
            return 'yyyy-mm-dd:{}:{}'.format(item, item)

        @staticmethod
        def unsign_valid(mock_obj, token, max_age=None):
            return 'foo'

        @staticmethod
        def unsign_expired(mock_obj, token, max_age=None):
            raise SignatureExpired('bar')

        @staticmethod
        def unsign_bad_signature(mock_obj, token, max_age=None):
            raise BadSignature('bar')

        @staticmethod
        def unsign_type_error(mock_obj, token, max_age=None):
            raise TypeError('bar')

    @override_settings(DAE_VERIFICATION_TOKEN_MAX_AGE=5)
    def test_max_age_applied(self):
        """Is the setting correctly read and applied?

        See '__init__()'-method."""

        c = EnhancedCrypto()

        self.assertEqual(c.max_age, 5)

    @mock.patch('django.core.signing.TimestampSigner.sign', new=MockSignUnsign.sign)
    def test_get_token_valid(self):
        """Is a token generated for a valid user object?

        See 'get_verification_token()'-method."""

        # create a User object to pass along
        u = get_user_model().objects.create(username='foo')
        c = EnhancedCrypto()
        t = c.get_verification_token(u)

        # asserts here!
        self.assertEqual(t, 'yyyy-mm-dd:foo:foo')

    def test_get_token_invalid(self):
        """Is a token generated for a valid user object?

        See 'get_verification_token()'-method."""

        c = EnhancedCrypto()

        with self.assertRaisesMessage(
            EnhancedCrypto.EnhancedCryptoException,
            "Something went wrong during crypto operations. This error message "
            "is unspecific to prevent any fingerprinting."
        ):
            t = c.get_verification_token(None)  # noqa

    @mock.patch('django.core.signing.TimestampSigner.unsign', new=MockSignUnsign.unsign_valid)
    def test_verify_token_valid(self):
        """A valid token returns a username.

        See 'verify_token()'-method."""

        c = EnhancedCrypto()
        u = c.verify_token(token='foo')

        self.assertEqual(u, 'foo')

    @mock.patch('django.core.signing.TimestampSigner.unsign', new=MockSignUnsign.unsign_expired)
    def test_verify_token_expired(self):
        """An expired token raises a specific exception.

        See 'verify_token()'-method."""

        c = EnhancedCrypto()

        with self.assertRaisesMessage(SignatureExpired, 'bar'):
            u = c.verify_token(token='foo')  # noqa

    @mock.patch('django.core.signing.TimestampSigner.unsign', new=MockSignUnsign.unsign_bad_signature)
    def test_verify_token_bad_signature(self):
        """'BadSignature' is caught and substituted by an own error.

        See 'verify_token()'-method."""

        c = EnhancedCrypto()

        with self.assertRaisesMessage(
            EnhancedCrypto.EnhancedCryptoException,
            "Something went wrong during crypto operations. This error "
            "message is unspecific to prevent any fingerprinting."
        ):
            u = c.verify_token(token='foo')  # noqa

    @mock.patch('django.core.signing.TimestampSigner.unsign', new=MockSignUnsign.unsign_type_error)
    def test_verify_token_type_error(self):
        """'TypeError' is caught and substituted by an own error.

        See 'verify_token()'-method."""

        c = EnhancedCrypto()

        with self.assertRaisesMessage(
            EnhancedCrypto.EnhancedCryptoException,
            "'verify_token()' was called without an actual token. "
            "You see this message, because this is probably a "
            "programming error/mistake."
        ):
            u = c.verify_token(token='foo')  # noqa
