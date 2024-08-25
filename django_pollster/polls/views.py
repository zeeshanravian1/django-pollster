"""
Polls Views Module

Description:
    - This module contains the views for the polls app.

"""

from django.db.models import F, QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
    """
    Index View

    Description:
        - This class is the index view for the polls app.

    Attributes:
        - `template_name (str):` The template name.
        - `context_object_name (str):` The context object name.

    """

    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self) -> QuerySet[Question]:  # type: ignore
        """
        Get Queryset Method

        Description:
            - This method returns the last five published questions.

        Args:
            - `None`

        Returns:
            - `queryset (QuerySet):` The queryset object.

        """

        return Question.objects.filter(  # pylint: disable=no-member
            pub_date__lte=timezone.now()
        ).order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    """
    Detail View

    Description:
        - This class is the detail view for the polls app.

    Attributes:
        - `model (Question):` The model.
        - `template_name (str):` The template name.

    """

    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.

        """

        return Question.objects.filter(  # pylint: disable=no-member
            pub_date__lte=timezone.now()
        )


class ResultsView(generic.DetailView):
    """
    Results View

    Description:
        - This class is the results view for the polls app.

    Attributes:
        - `model (Question):` The model.
        - `template_name (str):` The template name.

    """

    model = Question
    template_name = "polls/results.html"


def vote(request: HttpRequest, question_id) -> HttpResponse:
    """
    Vote View

    Description:
        - This method is the vote view for the polls app.

    Args:
        - `request (HttpRequest):` The request object.
        - `question_id (int):` The question id.

    Returns:
        - `response (HttpResponse):` The response object.

    """

    question: Question = get_object_or_404(klass=Question, pk=question_id)

    try:
        selected_choice: Choice = question.choice_set.get(  # type: ignore
            pk=request.POST["choice"]
        )

    except (KeyError, Choice.DoesNotExist):  # pylint: disable=no-member
        # Redisplay the question voting form.
        return render(
            request=request,
            template_name="polls/detail.html",
            context={
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )

    selected_choice.votes = F("votes") + 1
    selected_choice.save()

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(
        redirect_to=reverse(
            viewname="polls:results",
            args=(question.id,),  # type: ignore
        )
    )
