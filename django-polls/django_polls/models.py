"""
Polls Models Module

Description:
    - This module contains the models for the polls app.

"""

from datetime import timedelta

from django.contrib import admin
from django.db import models
from django.utils import timezone


class Question(models.Model):
    """
    Question Model

    Description:
        - This class represents a question object in the database.

    Attributes:
        - `question_text (CharField)`: The text of the question.
        - `pub_date (DateTimeField)`: The date the question was published.

    Methods:
        - `__str__(self) -> str`
        - `was_published_recently(self) -> bool`

    """

    question_text: models.CharField = models.CharField(max_length=2_00)
    pub_date: models.DateTimeField = models.DateTimeField(
        verbose_name="date published"
    )

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def __str__(self) -> str:  # pylint: disable=invalid-str-returned
        return self.question_text

    def was_published_recently(self) -> bool:
        """
        Was Published Recently Method

        Description:
            - This method checks if the question was published recently.

        Args:
            - `None`

        Returns:
            - `bool`: True if the question was published within the last day.

        """

        return (
            timezone.now() - timedelta(days=1)
            <= self.pub_date
            <= timezone.now()
        )


class Choice(models.Model):
    """
    Choice Model

    Description:
        - This class represents a choice object in the database.

    Attributes:
        - `question (ForeignKey)`: The question the choice is associated with.
        - `choice_text (CharField)`: The text of the choice.
        - `votes (IntegerField)`: The number of votes the choice has.

    Methods:
        - `__str__(self) -> str`

    """

    question: models.ForeignKey = models.ForeignKey(
        to=Question, on_delete=models.CASCADE
    )
    choice_text: models.CharField = models.CharField(max_length=2_00)
    votes: models.IntegerField = models.IntegerField(default=0)

    def __str__(self) -> str:  # pylint: disable=invalid-str-returned
        return self.choice_text
