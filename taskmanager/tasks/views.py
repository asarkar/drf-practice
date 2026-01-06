from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework.serializers import BaseSerializer

from .models import Task
from .serializers import (
    TaskCreateSerializer,
    TaskSerializer,
    TaskUpdateSerializer,
)


class TaskViewSet(viewsets.ModelViewSet[Task]):
    """ViewSet for handling Task CRUD operations."""

    queryset = Task.objects.all()

    def get_serializer_class(self) -> type[BaseSerializer[Task]]:
        """Return appropriate serializer class based on the request method."""
        match self.action:
            case "create":
                return TaskCreateSerializer
            case "update" | "partial_update":
                return TaskUpdateSerializer
            case _:
                return TaskSerializer

    def get_queryset(self) -> QuerySet[Task]:
        """Filter queryset based on query parameters."""
        qs = super().get_queryset()

        # Filter by completion status if provided
        completed = self.request.query_params.get("completed", None)
        if completed is not None:
            is_completed = completed.lower() == "true"
            qs = qs.filter(completed=is_completed)

        return qs
