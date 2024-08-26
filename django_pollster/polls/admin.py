"""
Polls Admin Module

Description:
    - This module contains the admin configuration for the polls app

"""

from django.contrib import admin

from .models import Question

admin.site.register(model_or_iterable=Question)
