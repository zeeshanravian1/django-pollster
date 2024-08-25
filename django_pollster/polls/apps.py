"""
Polls Apps Module

Description:
    - This module contains the configuration for the Polls app

"""

from django.apps import AppConfig


class PollsConfig(AppConfig):
    """
    Polls Configuration Class

    Description:
        - This class contains the configuration for the Polls app.

    Attributes:
        - `default_auto_field (str):` The default auto field for the app.
        - `name (str):` The name of the app.

    """

    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "polls"
