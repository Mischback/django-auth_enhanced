# -*- coding: utf-8 -*-
"""Includes tests targeting the app-specific admin classes.

    - target file: auth_enhanced/admin.py
    - included tags: 'admin'"""

# Python imports
from unittest import skip  # noqa

# Django imports
from django.test import override_settings, tag  # noqa

# app imports
from .utils.testcases import AuthEnhancedTestCase


@tag('admin')
class UserEnhancementAdminTests(AuthEnhancedTestCase):
    pass
