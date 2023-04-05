import plotly.graph_objs as go
import plotly.offline as pyo
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib.admin.views.decorators import staff_member_required

from . import utils
from .models import Lead, Survey, Response, Question


class HomePageView(TemplateView):
    template_name = "home.html"


class QuizView(View):
    def get(self, request):
        questions = Question.objects.all().order_by("number")
        options_dictionary = {}
        for question in questions:
            if question.type != "D":
                options_dictionary[question.number] = question.get_answer_options()
        return render(
            request,
            "quiz.html",
            {
                "questions": questions,
                "options_dictionary": options_dictionary,
            },
        )

    def post(self, request):
        # Save survey, lead and responses if req. met
        response_dict = dict(request.POST)

        for key in response_dict:
            # Convert lists into string text
            response_dict[key] = ", ".join(response_dict[key])
            if response_dict[key] is None or response_dict[key] == "":
                return JsonResponse(
                    {"response": "All fields required. Nice try!"},
                    status=400,
                )

        response_dict_keys = list(response_dict.keys())
        questions = Question.objects.all()
        email = response_dict["email"]

        try:
            lead = Lead.objects.create(email=email)
            survey = Survey.objects.create(lead=lead)
        except IntegrityError:
            return render(
                request,
                "error.html",
                {
                    "message": "You've already taken this survey, and we've mailed your Good Life Report!"
                },
                status=409,
            )

        for key in response_dict_keys:
            if key.isdigit():
                text = response_dict[key]
                for qn in questions:
                    if qn.number == int(key):
                        question = qn
                        Response(
                            survey=survey,
                            question=question,
                            text=text,
                        ).save()

        # Calculate and save lead score
        responses = Response.objects.filter(survey=survey).all()
        score = utils.calculate_score(responses)
        lead.score = score
        lead.save()

        print(score)

        # Generate pdf report
        report = utils.generate_report(questions, responses, email, score)

        # Mail the report
        utils.mail_report(report, email)

        return render(request, "thanks.html")


@staff_member_required
def analyze(request):
    # Analyze response percentages for each question into the results dictionary
    questions = Question.objects.exclude(type="D").order_by("number")
    results = {}

    for question in questions:
        responses = question.question_responses.all()
        answers = question.answers.all()
        answer_counts_dict = {}
        for answer in answers:
            answer_count = 0
            for response in responses:
                response_list = response.text.split(", ")
                if answer.text in response_list:
                    answer_count += 1
            answer_counts_dict[answer.text] = answer_count
        results[question.text] = answer_counts_dict

    # Generate pie charts using Plotly for each question
    charts = []
    for result in results:
        title = result
        data = {}
        labels = list(results[result].keys())
        values = list(results[result].values())
        data["labels"] = labels
        data["values"] = values
        trace = go.Pie(labels=data["labels"], values=data["values"], showlegend=True)
        layout = go.Layout(title=title, autosize=True)
        figure = go.Figure(data=[trace], layout=layout)
        figure.update_layout(
            title={
                "y": 1.0,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
            },
            legend={
                "yanchor": "top",
                "y": -0.1,
                "xanchor": "center",
                "x": 0.5,
            },
        )
        charts.append(pyo.plot(figure, output_type="div"))

    return render(
        request,
        "insights.html",
        {
            "charts": charts,
        },
    )
