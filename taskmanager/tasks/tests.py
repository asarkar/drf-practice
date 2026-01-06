from datetime import UTC

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Task


class TaskViewSetTests(APITestCase):
    """Tests for TaskViewSet."""

    def setUp(self) -> None:
        """Set up test data."""
        self.task1 = Task.objects.create(
            title="Task 1",
            description="Description 1",
            priority=1,
            completed=False,
        )
        self.task2 = Task.objects.create(
            title="Task 2",
            description="Description 2",
            priority=3,
            completed=True,
        )

    def test_list_tasks(self) -> None:
        """Test listing all tasks."""
        url = reverse("task-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        results = response.data["results"]
        self.assertEqual(len(results), 2)
        # Verify read-only fields are in response
        for task_data in results:
            self.assertIn("id", task_data)
            self.assertIn("created_at", task_data)
            self.assertIn("updated_at", task_data)

    def test_list_tasks_filter_completed_true(self) -> None:
        """Test filtering tasks by completed=true."""
        url = reverse("task-list")
        response = self.client.get(url, {"completed": "true"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Task 2")

    def test_list_tasks_filter_completed_false(self) -> None:
        """Test filtering tasks by completed=false."""
        url = reverse("task-list")
        response = self.client.get(url, {"completed": "false"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Task 1")

    def test_retrieve_task(self) -> None:
        """Test retrieving a single task."""
        url = reverse("task-detail", kwargs={"pk": self.task1.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Task 1")
        self.assertEqual(response.data["priority"], 1)
        # Verify read-only fields are in response
        self.assertEqual(response.data["id"], str(self.task1.pk))
        self.assertIn("created_at", response.data)
        self.assertIn("updated_at", response.data)

    def test_create_task(self) -> None:
        """Test creating a new task."""
        url = reverse("task-list")
        data = {
            "title": "New Task",
            "description": "New Description",
            "priority": 2,
            "completed": False,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)
        self.assertEqual(response.data["title"], "New Task")

    def test_create_task_priority_validation_too_low(self) -> None:
        """Test that priority below 1 is rejected."""
        url = reverse("task-list")
        data = {"title": "Invalid Task", "priority": 0}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("priority", response.data)

    def test_create_task_priority_validation_too_high(self) -> None:
        """Test that priority above 5 is rejected."""
        url = reverse("task-list")
        data = {"title": "Invalid Task", "priority": 6}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("priority", response.data)

    def test_update_task(self) -> None:
        """Test full update of a task."""
        url = reverse("task-detail", kwargs={"pk": self.task1.pk})
        data = {
            "title": "Updated Task",
            "description": "Updated Description",
            "priority": 5,
            "completed": True,
        }
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, "Updated Task")
        self.assertEqual(self.task1.priority, 5)
        self.assertTrue(self.task1.completed)

    def test_partial_update_task(self) -> None:
        """Test partial update of a task."""
        url = reverse("task-detail", kwargs={"pk": self.task1.pk})
        data = {"completed": True}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertTrue(self.task1.completed)
        self.assertEqual(self.task1.title, "Task 1")  # Unchanged

    def test_delete_task(self) -> None:
        """Test deleting a task."""
        url = reverse("task-detail", kwargs={"pk": self.task1.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 1)
        self.assertFalse(Task.objects.filter(pk=self.task1.pk).exists())

    def test_retrieve_nonexistent_task(self) -> None:
        """Test retrieving a task that doesn't exist."""
        import uuid

        url = reverse("task-detail", kwargs={"pk": uuid.uuid4()})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_task_ignores_readonly_fields(self) -> None:
        """Test that id, created_at, updated_at are ignored during create."""
        import uuid
        from datetime import datetime

        fake_id = uuid.uuid4()
        url = reverse("task-list")
        data = {
            "id": str(fake_id),
            "title": "New Task",
            "priority": 2,
            "created_at": "2020-01-01T00:00:00Z",
            "updated_at": "2020-01-01T00:00:00Z",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Fetch the created task from DB to verify
        created_task = Task.objects.get(title="New Task")
        # Verify the provided id was ignored (auto-generated instead)
        self.assertNotEqual(created_task.pk, fake_id)
        # Verify timestamps were auto-generated (not the fake ones from 2020)
        self.assertGreater(
            created_task.created_at,
            datetime(2023, 1, 1, tzinfo=UTC),
        )

    def test_update_task_ignores_readonly_fields(self) -> None:
        """Test that id, created_at, updated_at are ignored during update."""
        import uuid

        original_id = self.task1.pk
        original_created_at = self.task1.created_at
        fake_id = uuid.uuid4()

        url = reverse("task-detail", kwargs={"pk": self.task1.pk})
        data = {
            "id": str(fake_id),
            "title": "Updated Task",
            "description": "Updated",
            "priority": 3,
            "completed": True,
            "created_at": "2020-01-01T00:00:00Z",
            "updated_at": "2020-01-01T00:00:00Z",
        }
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        # Verify id was not changed
        self.assertEqual(self.task1.pk, original_id)
        # Verify created_at was not changed
        self.assertEqual(self.task1.created_at, original_created_at)

    def test_partial_update_task_ignores_readonly_fields(self) -> None:
        """Test that id, created_at, updated_at are ignored during partial update."""
        import uuid

        original_id = self.task1.pk
        original_created_at = self.task1.created_at
        fake_id = uuid.uuid4()

        url = reverse("task-detail", kwargs={"pk": self.task1.pk})
        data = {
            "id": str(fake_id),
            "created_at": "2020-01-01T00:00:00Z",
            "updated_at": "2020-01-01T00:00:00Z",
        }
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        # Verify id was not changed
        self.assertEqual(self.task1.pk, original_id)
        # Verify created_at was not changed
        self.assertEqual(self.task1.created_at, original_created_at)
