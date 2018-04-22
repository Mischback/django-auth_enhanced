# -*- coding: utf-8 -*-

# Django imports
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

# app imports
from auth_enhanced.forms import SignupForm


class SignupView(CreateView):
    """This class based view handles the registration of new users."""

    form_class = SignupForm
    success_url = reverse_lazy('auth_enhanced:login')
    template_name = 'auth_enhanced/signup.html'
