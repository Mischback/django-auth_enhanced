# -*- coding: utf-8 -*-

# Django imports
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView

# app imports
from auth_enhanced.forms import EmailVerificationForm, SignupForm


class EmailVerificationView(FormView):
    """Provides the frontend to verify user's email addresses."""

    form_class = EmailVerificationForm
    success_url = reverse_lazy('auth_enhanced:login')
    template_name = 'auth_enhanced/email_verification.html'

    def form_valid(self, form):
        """This method is executed, if the form is valid. This triggers the
        activation of the user."""

        # actually activate the user by using a form-method
        form.activate_user()

        return super(EmailVerificationView, self).form_valid(form)

    def get(self, request, verification_token=None, *args, **kwargs):
        """The 'get()'-method is overwritten to accept the token in the url or
        by form."""

        if verification_token:

            # build the form manually and let it be validated
            form = self.get_form_class()(
                data={
                    'token': verification_token,
                }
            )

            if form.is_valid():
                # if the form is already valid (meaning: the token is valid)
                #   let Django handle all further steps
                return self.form_valid(form)
            else:
                # if the form could not be validated (meaning: the token is not
                #   valid), show the default interface for manual submit.
                return redirect('auth_enhanced:email-verification')

        else:
            # this will take care of showing the form
            return super(EmailVerificationView, self).get(request, *args, **kwargs)


class SignupView(CreateView):
    """This class based view handles the registration of new users."""

    form_class = SignupForm
    success_url = reverse_lazy('auth_enhanced:login')
    template_name = 'auth_enhanced/signup.html'
