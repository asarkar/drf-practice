from typing import Any

from rest_framework import serializers

from .models import Task


class BaseTaskSerializer(serializers.ModelSerializer[Task]):
    """Base serializer for tasks with common fields.

    This class cannot be instantiated directly - use a concrete subclass.
    """

    class Meta:
        model = Task
        fields = ["title", "description", "priority", "completed"]

    def __new__(cls, *args: Any, **kwargs: Any) -> BaseTaskSerializer:
        if cls is BaseTaskSerializer:
            raise TypeError(f"{cls.__name__} cannot be instantiated directly")
        # Let DRF handle many=True (returns ListSerializer) and other special cases
        return super().__new__(cls, *args, **kwargs)


class TaskSerializer(BaseTaskSerializer):
    """Serializer for the Task model."""

    class Meta(BaseTaskSerializer.Meta):
        fields = ["id", *BaseTaskSerializer.Meta.fields, "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class TaskCreateSerializer(BaseTaskSerializer):
    """Serializer for creating tasks."""

    pass


class TaskUpdateSerializer(BaseTaskSerializer):
    """Serializer for updating tasks."""

    class Meta(BaseTaskSerializer.Meta):
        extra_kwargs = {
            "title": {"required": False},
            "description": {"required": False},
            "priority": {"required": False},
            "completed": {"required": False},
        }
