"""
Polls URLs Module

Description:
    - This module contains the URL patterns for the polls app.

"""

from django.urls import path
from django.urls.resolvers import URLPattern

from . import views

app_name: str = "polls"

urlpatterns: list[URLPattern] = [
    path(route="", view=views.index, name="index"),
    path(route="<int:question_id>/", view=views.detail, name="detail"),
    path(
        route="<int:question_id>/results/", view=views.results, name="results"
    ),
    path(route="<int:question_id>/vote/", view=views.vote, name="vote"),
]
