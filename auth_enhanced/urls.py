# -*- coding: utf-8 -*-
"""django-auth_enhanced: URL configuration

Contains app specific URLS to decouple them from the project's URL config.

Include them in the project's 'urls.py', i.e.
    url(r'^auth/', include('auth_enhanced.urls')),

Please note, that if you want to modify the actual url patterns, you may
copy/paste single lines from this file into your config. Be aware, that you
may have to adjust your imports accordingly."""

# Django imports
from django.conf.urls import url
from django.contrib.auth.views import LoginView

# specify the app name
app_name = 'auth_enhanced'

# define the urls to match
urlpatterns = [
    # TODO: 'url' got replaced by 'path' in Django 2.0
    url(r'^login/$', LoginView.as_view(template_name='auth_enhanced/login.html'), name='login'),
]
