from django.urls import path

from .views import QuizListView, QuizQuestionListView, RandomQuestionView

app_name = "quizzes"

urlpatterns = [
    path("", QuizListView.as_view(), name="quiz-list"),
    path("r/<str:topic>/", RandomQuestionView.as_view(), name="question-random"),
    path("q/<str:topic>/", QuizQuestionListView.as_view(), name="question-list"),
]
