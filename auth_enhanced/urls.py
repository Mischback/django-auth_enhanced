# -*- coding: utf-8 -*-
"""Contains app specific URLS to decouple them from the project's URL config.

Include them in the project's 'urls.py', i.e.
    url(r'^auth/', include('auth_enhanced.urls')),

Please note, that if you want to modify the actual url patterns, you may
copy/paste single lines from this file into your config. Be aware, that you
may have to adjust your imports accordingly."""

# Django imports
from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView

# app imports
from auth_enhanced.views import EmailVerificationView, SignupView

# from django.urls import register_converter


# specify the app name
app_name = 'auth_enhanced'


# class VerificationTokenConverter:
#     """FIXME: This seems to work from Django 2.0"""
#     regex = '[a-zA-Z0-9]+:[a-zA-Z0-9]+:[a-zA-Z0-9]+'

#     def to_python(self, value):
#         return value

#     def to_url(self, value):
#         return '{}'.format(value)

# # register the custom converter
# register_converter(VerificationTokenConverter, 'token')

# define the urls to match
# TODO: 'url' got replaced by 'path' in Django 2.0
urlpatterns = [
    url(r'^login/$', LoginView.as_view(template_name='auth_enhanced/login.html'), name='login'),
    url(r'^logout/$', LogoutView.as_view(template_name='auth_enhanced/logout.html'), name='logout'),
    url(r'^signup/$', SignupView.as_view(), name='signup'),
    # 'email-verification' may be called with or without an url parameter
    url(
        r'^verify-email(?:/(?P<verification_token>[a-zA-Z0-9:]+))?/$',
        EmailVerificationView.as_view(),
        name='email-verification'
    ),
]
