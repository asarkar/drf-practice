import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Task(models.Model):
    """Model representing a task in the system."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True, null=True)
    priority = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        """String representation of the task."""
        return self.title
