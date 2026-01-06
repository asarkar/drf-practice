from rest_framework import serializers

from .models import Answer, Question, Quiz


class QuizSerializer(serializers.ModelSerializer[Quiz]):
    class Meta:
        model = Quiz
        fields = ["title"]


class AnswerSerializer(serializers.ModelSerializer[Answer]):
    class Meta:
        model = Answer
        fields = ["id", "answer_text", "is_right"]


class RandomQuestionSerializer(serializers.ModelSerializer[Question]):
    # https://www.django-rest-framework.org/api-guide/fields/#serializermethodfield
    # answers = serializers.SerializerMethodField()
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ["title", "answers"]

    # def get_answers(self, obj: Question) -> list[str]:
    #     return list(obj.answers.values_list("answer_text", flat=True))


class QuestionSerializer(serializers.ModelSerializer[Question]):
    answers = AnswerSerializer(many=True, read_only=True)
    quiz = QuizSerializer(read_only=True)

    class Meta:
        model = Question
        fields = ["quiz", "title", "answers"]
