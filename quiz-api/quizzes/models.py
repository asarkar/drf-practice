from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    class Meta:
        # `verbose_name*` are used for display in the Django Admin
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Quiz(models.Model):
    class Meta:
        # `verbose_name*` are used for display in the Django Admin
        verbose_name = _("Quiz")
        verbose_name_plural = _("Quizzes")
        ordering = ("id",)

    title = models.CharField(_("Quiz Title"), max_length=255, default=_("New Quiz"))
    category = models.ForeignKey(Category, default=1, on_delete=models.DO_NOTHING)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class Updated(models.Model):
    date_updated = models.DateTimeField(_("Last Updated"), auto_now=True)

    class Meta:
        abstract = True


class Question(Updated):
    class Meta:
        # `verbose_name*` are used for display in the Django Admin
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ("id",)

    SCALE = (
        (0, _("Fundamental")),
        (1, _("Beginner")),
        (2, _("Intermediate")),
        (2, _("Advanced")),
        (4, _("Expert")),
    )

    TYPE = ((0, _("Multiple Choice")),)

    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.DO_NOTHING)
    technique = models.IntegerField(_("Type of Question"), choices=TYPE, default=0)
    title = models.CharField(_("Title"), max_length=255)
    difficulty = models.IntegerField(_("Difficulty"), choices=SCALE, default=0)
    date_created = models.DateTimeField("Date Created", auto_now_add=True)
    is_active = models.BooleanField(_("Active Status"), default=True)

    def __str__(self) -> str:
        return self.title


class Answer(Updated):
    class Meta:
        # `verbose_name*` are used for display in the Django Admin
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")
        ordering = ("id",)

    question = models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE)
    answer_text = models.CharField(_("Answer Text"), max_length=255)
    is_right = models.BooleanField(default=False)
