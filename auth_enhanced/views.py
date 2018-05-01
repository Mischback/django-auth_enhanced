# -*- coding: utf-8 -*-

# Django imports
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView

# app imports
from auth_enhanced.forms import EmailVerificationForm, SignupForm


class EmailVerificationView(FormView):

    form_class = EmailVerificationForm
    success_url = reverse_lazy('auth_enhanced:login')
    template_name = 'auth_enhanced/email_verification.html'

    def form_valid(self, form):

        # actually activate the user by using a form-method
        form.activate_user()

        return super(EmailVerificationView, self).form_valid(form)


class SignupView(CreateView):
    """This class based view handles the registration of new users."""

    form_class = SignupForm
    success_url = reverse_lazy('auth_enhanced:login')
    template_name = 'auth_enhanced/signup.html'
