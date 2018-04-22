# -*- coding: utf-8 -*-
"""Contains app-specific forms."""

# Django imports
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _

# app imports
from auth_enhanced.settings import DAE_MODE_EMAIL_ACTIVATION


class SignupForm(UserCreationForm):
    """Extends Django's form to create new User objects.

    Several things are done here:
        - enforce unique email addresses"""

    def __init__(self, *args, **kwargs):
        """Custom constructor"""

        # call the parent constructor
        super(SignupForm, self).__init__(*args, **kwargs)

        # if the email address is not mandatorily required, remove it from the form
        if not settings.DAE_OPERATION_MODE == DAE_MODE_EMAIL_ACTIVATION:
            del self.fields[self._meta.model.EMAIL_FIELD]

    def clean(self):
        """Custom validation method to ensure some constraints on user's input.

        1) ensures, that the email is present (and valid), if one is required
        2) ensures, that the given email address is unique"""

        # grab the data
        cleaned_data = super(SignupForm, self).clean()

        # perform some email validation tasks
        email = cleaned_data.get(self._meta.model.EMAIL_FIELD)

        # enfoce a valid email address (if required)
        if settings.DAE_OPERATION_MODE == DAE_MODE_EMAIL_ACTIVATION and not email:
            raise ValidationError(
                _('A valid email address is required!'),
                code='valid_email_required'
            )

        # enforce a unique email address
        email_query = {
            self._meta.model.EMAIL_FIELD: email,
        }
        try:
            foo = self._meta.model.objects.get(**email_query)
        except self._meta.model.DoesNotExist:
            # TODO: if this works, just 'pass' the exception
            print('Email address does not yet exist! Yeah!')

        # pass the data on
        return cleaned_data
