# -*- coding: utf-8 -*-
"""Contains app-specific forms."""

# Django imports
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.signing import SignatureExpired
from django.forms import CharField, Form, ValidationError
from django.utils.translation import ugettext_lazy as _

# app imports
from auth_enhanced.crypto import EnhancedCrypto
from auth_enhanced.models import UserEnhancement
from auth_enhanced.settings import (
    DAE_CONST_MODE_EMAIL_ACTIVATION, DAE_CONST_MODE_MANUAL_ACTIVATION,
)


class EmailVerificationForm(Form):
    """Handles email verification by dealing with submitted tokens."""

    token = CharField()

    username = None

    # let's mimic the behaviour of 'UserCreationForm'. And yes, this is dirty (;
    class Meta:
        # be as pluggable as possible, so django.contrib.auth's User is not
        #   directly referenced
        model = get_user_model()
    _meta = Meta

    def clean_token(self):
        """This method actually take care of token verification."""

        token = self.cleaned_data['token']

        try:
            self.username = EnhancedCrypto().verify_token(token)
            # print("[EmailVerificationForm] successfully verified token for '{}'".format(self.username))
        except SignatureExpired:
            raise ValidationError(
                _(
                    "It seems like you have submitted a valid verification "
                    "token, that is expired. Be aware, that verification "
                    "tokens are considered valid for {} seconds and must be "
                    "used within that time period.".format(settings.DAE_VERIFICATION_TOKEN_MAX_AGE)
                ),
                code='dae_token_expired'
            )
        except EnhancedCrypto.EnhancedCryptoException:
            # TODO: provide some meaningful error message here
            raise ValidationError(
                _("Your submitted token could not be verified!"),
                code='dae_token_could_not_be_verified'
            )

        return token

    def activate_user(self):
        """If the submitted token is verified, the account can safely get activated."""

        user_to_be_activated = None
        user_query = {
            self._meta.model.USERNAME_FIELD: self.username,
        }
        try:
            user_to_be_activated = self._meta.model.objects.get(**user_query)
        except self._meta.model.DoesNotExist:
            # the user could not be found
            raise

        # the following part could be done more defensively, if guarded with
        #   'if user_to_be_activated:'
        try:
            enhancement = UserEnhancement.objects.get(user=user_to_be_activated)
        except UserEnhancement.DoesNotExist:
            # logical database integrity FAILED
            # TODO: Should this be raised? Or handle it gracefully by creating an enhancement-object?
            raise

        # update the verification status
        enhancement.email_verification_status = enhancement.EMAIL_VERIFICATION_COMPLETED
        enhancement.save(update_fields=['email_verification_status'])

        # activate the user
        user_to_be_activated.is_active = True
        user_to_be_activated.save(update_fields=['is_active'])


class SignupForm(UserCreationForm):
    """Extends Django's form to create new User objects.

    Several things are done here:
        - enforce unique email addresses"""

    class Meta:
        # be as pluggable as possible, so django.contrib.auth's User is not
        #   directly referenced
        # adding 'EMAIL_FIELD' here, but it may be removed in '__init__', if
        #   the email address is not required
        model = get_user_model()
        fields = (
            model.USERNAME_FIELD,
            model.EMAIL_FIELD,
            'password1', 'password2'
        )

    def __init__(self, *args, **kwargs):
        """Custom constructor"""

        # call the parent constructor
        super(SignupForm, self).__init__(*args, **kwargs)

        # if the email address is not mandatorily required, remove it from the form
        if not settings.DAE_OPERATION_MODE == DAE_CONST_MODE_EMAIL_ACTIVATION:
            del self.fields[self._meta.model.EMAIL_FIELD]

    def clean(self):
        """Custom validation method to ensure some constraints on user's input.

        1) ensures, that the email is present (and valid), if one is required
        2) ensures, that the given email address is unique"""

        # grab the data
        cleaned_data = super(SignupForm, self).clean()

        # perform some email validation tasks
        email = cleaned_data.get(self._meta.model.EMAIL_FIELD)

        # enforce a valid email address (if required)
        if settings.DAE_OPERATION_MODE == DAE_CONST_MODE_EMAIL_ACTIVATION and not email:
            raise ValidationError(
                _('A valid email address is required!'),
                code='valid_email_required'
            )

        # enforce a unique email address
        # TODO / FIXME: As of now, this code is already doing things, if the
        #   email address is a required field, because otherwise this form
        #   won't handle the email-field, even if specified.
        #   The below code has to be applied to all forms, that can change a
        #   User object! How to do this? Write a Mixin / MultiInheritance?
        # Wondering about this crazy syntax? To keep the app as pluggable as
        #   possible, the 'email'-field is not referenced directly. But this
        #   requires to look for the content of that field, but it can't be
        #   used as keyword-paramter in 'get()'.
        already_used_email = None
        email_query = {
            self._meta.model.EMAIL_FIELD: email,
        }
        try:
            already_used_email = self._meta.model.objects.get(**email_query)
        except self._meta.model.DoesNotExist:
            # if the exception is thrown, the email address is not in the database,
            #   just what is expected/required! Just go on!
            pass

        # if the try/except above didn't fail, we have an User-object in
        #   'already_used_email'. This means, that this email address is already
        #   in use and may not be registered again.
        #   Keep in mind to not disclose any more information at this point!
        if already_used_email:
            raise ValidationError(
                _('This email address is already in use! Email addresses may only be registered once!'),
                code='email_not_unique'
            )

        # pass the data on
        return cleaned_data

    def save(self, commit=True):
        """This method ensures, that the 'is_active'-flag is filled according
        to the app's settings."""

        # call the parent's 'save()' without saving
        user = super(SignupForm, self).save(commit=False)

        # 'DAE_CONST_MODE_MANUAL_ACTIVATION' or 'DAE_CONST_MODE_EMAIL_ACTIVATION'
        # implies 'is_active' = False
        if settings.DAE_OPERATION_MODE in (DAE_CONST_MODE_MANUAL_ACTIVATION, DAE_CONST_MODE_EMAIL_ACTIVATION):
            user.is_active = False

        if commit:
            user.save()

        return user
