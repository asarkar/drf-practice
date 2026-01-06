from rest_framework import serializers

from .models import Task


class AbstractTaskSerializer(serializers.ModelSerializer[Task]):
    """Abstract base serializer for tasks."""

    class Meta:
        model = Task
        fields = ["title", "description", "priority", "completed"]
        abstract = True


class TaskSerializer(AbstractTaskSerializer):
    """Serializer for the Task model."""

    class Meta(AbstractTaskSerializer.Meta):
        fields = ["id", *AbstractTaskSerializer.Meta.fields, "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class TaskCreateSerializer(AbstractTaskSerializer):
    """Serializer for creating tasks."""

    pass


class TaskUpdateSerializer(AbstractTaskSerializer):
    """Serializer for updating tasks."""

    class Meta(AbstractTaskSerializer.Meta):
        extra_kwargs = {
            "title": {"required": False},
            "description": {"required": False},
            "priority": {"required": False},
            "completed": {"required": False},
        }
