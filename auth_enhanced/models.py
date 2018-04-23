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
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

# app imports
from auth_enhanced.exceptions import AuthEnhancedException


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
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enhancement'
    )

    class UserEnhancementException(AuthEnhancedException):
        """This exception indicates, that something went wrong inside this model"""
        pass

    @classmethod
    def callback_create_enhancement_object(cls, sender, instance, created, user_obj=None, user_id=None, **kwargs):
        """Returns a new instance of UserEnhancement, tied to a User-object"""

        # only execute this code on object creation, not on every single save()
        if created:
            if instance:
                new_enhancement = cls(user=instance)
            elif user_obj:
                new_enhancement = cls(user=user_obj)
            elif user_id:
                try:
                    new_enhancement = cls(user=get_user_model().objects.get(pk=user_id))
                except get_user_model().DoesNotExist:
                    raise cls.UserEnhancementException(_('The given user id does not exist!'))
            else:
                raise cls.UserEnhancementException(_('Could not determine a valid user object!'))

            return new_enhancement
        else:
            return None

    @property
    def email_is_verified(self):
        """Returns a simple boolean value, depending on the 'email_verification_status'"""

        if self.email_verification_status == self.EMAIL_VERIFICATION_COMPLETED:
            return True

        return False
