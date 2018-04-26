# -*- coding: utf-8 -*-
"""Provides a minimal URL configuration for tests and development.

This file mimics a project's URL configuration, in order to run the app during
development and testing.

TODO: create a 'root-view' under the URL '/', which renders some basic template."""

# Django imports
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='base.html'), name='home'),
    url(r'^', include('auth_enhanced.urls')),
    url(r'^admin/', admin.site.urls),
]
