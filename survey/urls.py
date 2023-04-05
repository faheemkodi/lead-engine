from django.urls import path

from .views import HomePageView, QuizView, analyze


app_name = "survey"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("quiz/", QuizView.as_view(), name="quiz"),
    path("survey/insights/", analyze, name="insights"),
]
