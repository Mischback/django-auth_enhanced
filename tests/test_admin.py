# -*- coding: utf-8 -*-
"""Includes tests targeting the app-specific forms.

    - target file: auth_enhanced/admin.py
    - included tags: 'admin'"""

# Python imports
from unittest import skip  # noqa

# Django imports
from django.test import override_settings, tag  # noqa

# app imports
from .utils.testcases import AuthEnhancedNoSignalsTestCase


@tag('admin')
class UserEnhancementAdminTests(AuthEnhancedNoSignalsTestCase):
    pass
