from typing import Any

from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Question, Quiz
from .serializers import QuestionSerializer, QuizSerializer, RandomQuestionSerializer


class QuizListView(generics.ListAPIView[Quiz]):
    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()


class RandomQuestionView(APIView):
    def get(self, request: Request, format: str | None = None, **kwargs: Any) -> Response:
        question = Question.objects.filter(quiz__title=kwargs["topic"]).order_by("?").first()
        if question is not None:
            serializer = RandomQuestionSerializer(question)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)


class QuizQuestionListView(APIView):
    def get(self, request: Request, format: str | None = None, **kwargs: Any) -> Response:
        questions = Question.objects.filter(quiz__title=kwargs["topic"])
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)
