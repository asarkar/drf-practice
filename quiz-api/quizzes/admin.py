from django.contrib import admin

from .models import Answer, Category, Question, Quiz

# mypy: disable-error-code="type-arg"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("id", "title")


class AnswerInlineModelAdmin(admin.TabularInline):
    model = Answer
    fields = ["answer_text", "is_right"]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fields = ["title", "quiz"]
    list_display = ("title", "quiz", "date_updated")
    inlines = [AnswerInlineModelAdmin]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("answer_text", "is_right", "question")
    model = Answer
