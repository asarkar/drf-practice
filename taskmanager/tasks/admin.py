from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = ("title", "priority", "completed", "created_at")
    list_filter = ("completed", "priority")
    search_fields = ("title", "description")
    readonly_fields = ("id", "created_at", "updated_at")
