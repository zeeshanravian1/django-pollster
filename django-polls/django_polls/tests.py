"""
Polls Tests Module

Description:
    - This module contains the test cases for the polls app.

"""

from datetime import datetime, timedelta

from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question


class QuestionModelTests(TestCase):
    """
    Question Model Test Cases

    Description:
        - This class contains the test cases for the Question model.

    Attributes:
        - `None`

    Methods:
        - `test_was_published_recently_with_future_question(self) -> None`:
            - Description:
                - This method tests the was_published_recently method of the
                Question model.
                - It tests if the method returns False for questions whose
                pub_date is in the future.

            - Args:
                - `None`

            - Returns:
                - `None`

        - `test_was_published_recently_with_old_question(self) -> None`:
            - Description:
                - This method tests the was_published_recently method of the
                Question model.
                - It tests if the method returns False for questions whose
                pub_date is older than 1 day.

            - Args:
                - `None`

            - Returns:
                - `None`

        - `test_was_published_recently_with_recent_question(self) -> None`:
            - Description:
                - This method tests the was_published_recently method of the
                Question model.
                - It tests if the method returns True for questions whose
                pub_date is within the last day.

            - Args:
                - `None`

            - Returns:
                - `None`

    """

    def test_was_published_recently_with_future_question(self) -> None:
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """

        time: datetime = timezone.now() + timedelta(days=30)
        future_question: Question = Question(pub_date=time)

        self.assertIs(
            expr1=future_question.was_published_recently(),
            expr2=False,
            msg="Future questions should not be published recently.",
        )

    def test_was_published_recently_with_old_question(self) -> None:
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """

        time: datetime = timezone.now() - timedelta(days=1, seconds=1)
        old_question: Question = Question(pub_date=time)

        self.assertIs(
            expr1=old_question.was_published_recently(),
            expr2=False,
            msg="Old questions should not be published recently.",
        )

    def test_was_published_recently_with_recent_question(self) -> None:
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """

        time: datetime = timezone.now() - timedelta(
            hours=23, minutes=59, seconds=59
        )
        recent_question: Question = Question(pub_date=time)

        self.assertIs(
            expr1=recent_question.was_published_recently(),
            expr2=True,
            msg="Recent questions should be published recently.",
        )


def create_question(question_text, days) -> Question:
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """

    time: datetime = timezone.now() + timedelta(days=days)

    return Question.objects.create(  # pylint: disable=no-member
        question_text=question_text, pub_date=time
    )


class QuestionIndexViewTests(TestCase):
    """
    Question Index View Test Cases

    Description:
        - This class contains the test cases for the Question Index View.

    Attributes:
        - `None`

    Methods:
        - `test_no_questions(self) -> None`:
            - Description:
                - This method tests if an appropriate message is displayed
                when no questions exist.

            - Args:
                - `None`

            - Returns:
                - `None`

        - `test_past_question(self) -> None`:
            - Description:
                - This method tests if questions with a pub_date in the past
                are displayed on the index page.

            - Args:
                - `None`

            - Returns:
                - `None`

        - `test_future_question(self) -> None`:
            - Description:
                - This method tests if questions with a pub_date in the future
                aren't displayed on the index page.

            - Args:
                - `None`

            - Returns:
                - `None`

        - `test_future_question_and_past_question(self) -> None`:
            - Description:
                - This method tests if only past questions are displayed even
                if both past and future questions exist.

            - Args:
                - `None`

            - Returns:
                - `None`

        - `test_two_past_questions(self) -> None`:
            - Description:
                - This method tests if the questions index page may display
                multiple questions.

            - Args:
                - `None`

            - Returns:
                - `None`

    """

    def test_no_questions(self) -> None:
        """
        If no questions exist, an appropriate message is displayed.
        """

        response: HttpResponse = self.client.get(  # type: ignore
            path=reverse(viewname="polls:index")
        )

        self.assertEqual(
            first=response.status_code,
            second=2_00,
            msg="Status code should be 200.",
        )
        self.assertContains(response=response, text="No polls are available.")
        self.assertQuerySetEqual(
            qs=response.context["latest_question_list"],  # type: ignore
            values=[],
        )

    def test_past_question(self) -> None:
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """

        question: Question = create_question(
            question_text="Past question.", days=-30
        )
        response: HttpResponse = self.client.get(  # type: ignore
            path=reverse(viewname="polls:index")
        )

        self.assertQuerySetEqual(
            qs=response.context["latest_question_list"],  # type: ignore
            values=[question],
        )

    def test_future_question(self) -> None:
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """

        create_question(question_text="Future question.", days=30)
        response: HttpResponse = self.client.get(  # type: ignore
            path=reverse(viewname="polls:index")
        )

        self.assertContains(response=response, text="No polls are available.")
        self.assertQuerySetEqual(
            qs=response.context["latest_question_list"],  # type: ignore
            values=[],
        )

    def test_future_question_and_past_question(self) -> None:
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """

        question: Question = create_question(
            question_text="Past question.", days=-30
        )
        create_question(question_text="Future question.", days=30)
        response: HttpResponse = self.client.get(  # type: ignore
            path=reverse(viewname="polls:index")
        )

        self.assertQuerySetEqual(
            qs=response.context["latest_question_list"],  # type: ignore
            values=[question],
        )

    def test_two_past_questions(self) -> None:
        """
        The questions index page may display multiple questions.
        """

        question1: Question = create_question(
            question_text="Past question 1.", days=-30
        )
        question2: Question = create_question(
            question_text="Past question 2.", days=-5
        )
        response: HttpResponse = self.client.get(  # type: ignore
            path=reverse(viewname="polls:index")
        )

        self.assertQuerySetEqual(
            qs=response.context["latest_question_list"],  # type: ignore
            values=[question2, question1],
        )


class QuestionDetailViewTests(TestCase):
    """
    Question Detail View Test Cases

    Description:
        - This class contains the test cases for the Question Detail View.

    Attributes:
        - `None`

    Methods:
        - `test_future_question(self) -> None`:
            - Description:
                - This method tests if the detail view of a question with a
                pub_date in the future returns a 404 not found.

            - Args:
                - `None`

            - Returns:
                - `None`

        - `test_past_question(self) -> None`:
            - Description:
                - This method tests if the detail view of a question with a
                pub_date in the past displays the question's text.

            - Args:
                - `None`

            - Returns:
                - `None`

    """

    def test_future_question(self) -> None:
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """

        future_question: Question = create_question(
            question_text="Future question.", days=5
        )
        url: str = reverse(
            viewname="polls:detail",
            args=(future_question.id,),  # type: ignore
        )
        response: HttpResponse = self.client.get(path=url)  # type: ignore

        self.assertEqual(
            first=response.status_code,
            second=404,
            msg="The status code should be 404 as the question is "
            "in the future.",
        )

    def test_past_question(self) -> None:
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """

        past_question: Question = create_question(
            question_text="Past Question.", days=-5
        )
        url: str = reverse(
            viewname="polls:detail",
            args=(past_question.id,),  # type: ignore
        )
        response: HttpResponse = self.client.get(path=url)  # type: ignore

        self.assertContains(
            response=response, text=past_question.question_text
        )
