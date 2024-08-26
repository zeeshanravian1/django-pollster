"""
Polls Admin Module

Description:
    - This module contains the admin configuration for the polls app.

"""

from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    """
    Choice Inline Class

    Description:
        - This class represents the inline configuration for the Choice model.

    Attributes:
        - `model (Choice)`: The Choice model.
        - `extra (int)`: The number of extra fields to display.

    Methods:
        - `None`

    """

    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """
    Question Admin Class

    Description:
        - This class represents the admin configuration for the Question model.

    Attributes:
        - `fieldsets (list)`: The fieldsets to display.
        - `inlines (list)`: The inlines to display.
        - `list_display (list)`: The fields to display in the list view.
        - `list_filter (list)`: The fields to filter by.
        - `search_fields (list)`: The fields to search by.

    Methods:
        - `None`

    """

    fieldsets = [
        (None, {"fields": ["question_text"]}),
        (
            "Date information",
            {"fields": ["pub_date"], "classes": ["collapse"]},
        ),
    ]
    inlines = [ChoiceInline]

    list_display = [
        "question_text",
        "pub_date",
        "was_published_recently",
    ]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]


admin.site.register(model_or_iterable=Question, admin_class=QuestionAdmin)
