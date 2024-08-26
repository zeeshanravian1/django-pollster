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
    path(route="", view=views.IndexView.as_view(), name="index"),
    path(
        route="<int:pk>/",
        view=views.DetailView.as_view(),
        name="detail",
    ),
    path(
        route="<int:pk>/results/",
        view=views.ResultsView.as_view(),
        name="results",
    ),
    path(route="<int:question_id>/vote/", view=views.vote, name="vote"),
]
