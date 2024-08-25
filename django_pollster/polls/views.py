"""
Polls Views Module

Description:
    - This module contains the views for the polls app.

"""

from django.db.models import F, QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Choice, Question


def index(request: HttpRequest) -> HttpResponse:
    """
    Index View

    Description:
        - This method is the index view for the polls app.

    Args:
        - `request (HttpRequest):` The request object.

    Returns:
        - `response (HttpResponse):` The response object.

    """

    latest_question_list: QuerySet[Question] = (  # type: ignore
        Question.objects.order_by("-pub_date")[:5]  # pylint: disable=no-member
    )
    context: dict[str, QuerySet[Question]] = {  # type: ignore
        "latest_question_list": latest_question_list,
    }
    return render(
        request=request, template_name="polls/index.html", context=context
    )


def detail(request: HttpRequest, question_id) -> HttpResponse:
    """
    Detail View

    Description:
        - This method is the detail view for the polls app.

    Args:
        - `request (HttpRequest):` The request object.
        - `question_id (int):` The question id.

    Returns:
        - `response (HttpResponse):` The response object.

    """

    question: Question = get_object_or_404(klass=Question, pk=question_id)

    return render(
        request=request,
        template_name="polls/detail.html",
        context={"question": question},
    )


def results(request: HttpRequest, question_id) -> HttpResponse:
    """
    Results View

    Description:
        - This method is the results view for the polls app.

    Args:
        - `request (HttpRequest):` The request object.
        - `question_id (int):` The question id.

    Returns:
        - `response (HttpResponse):` The response object.

    """

    question: Question = get_object_or_404(Question, pk=question_id)

    return render(
        request=request,
        template_name="polls/results.html",
        context={"question": question},
    )


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
