import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from src.app import app

client = TestClient(app)


@pytest.fixture
def mock_task_model():
    """Mock the TaskModel for testing."""
    with patch("apps.tasks.routes.task_model") as mock_model:
        yield mock_model


@pytest.fixture
def sample_task():
    """Sample task data for testing."""
    from datetime import datetime

    return {
        "id": "507f1f77bcf86cd799439011",
        "title": "Test Task",
        "description": "Test Description",
        "done": False,
        "created_at": datetime(2023, 1, 1, 12, 0, 0),
        "updated_at": datetime(2023, 1, 1, 12, 0, 0),
    }


class TestHealthAPI:
    """Test health check endpoint."""

    def test_health_check(self):
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestTaskAPI:
    """Test task API endpoints."""

    def test_create_task(self, mock_task_model, sample_task):
        """Test creating a task."""
        mock_task_model.create_task.return_value = sample_task

        response = client.post(
            "/tasks/", json={"title": "Test Task", "description": "Test Description"}
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Task"
        assert data["description"] == "Test Description"
        assert data["done"] is False

    def test_get_tasks(self, mock_task_model, sample_task):
        """Test getting all tasks."""
        mock_task_model.get_tasks.return_value = [sample_task]

        response = client.get("/tasks/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Test Task"

    def test_get_task(self, mock_task_model, sample_task):
        """Test getting a specific task."""
        mock_task_model.get_task_by_id.return_value = sample_task

        response = client.get("/tasks/507f1f77bcf86cd799439011")

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Task"

    def test_get_task_not_found(self, mock_task_model):
        """Test getting non-existent task."""
        mock_task_model.get_task_by_id.return_value = None

        response = client.get("/tasks/507f1f77bcf86cd799439011")

        assert response.status_code == 404
        assert response.json() == {"detail": "Task not found"}

    def test_update_task(self, mock_task_model, sample_task):
        """Test updating a task."""
        updated_task = sample_task.copy()
        updated_task["title"] = "Updated Task"
        mock_task_model.update_task.return_value = updated_task

        response = client.put(
            "/tasks/507f1f77bcf86cd799439011", json={"title": "Updated Task"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Task"

    def test_update_task_empty_body(self):
        """Test updating with empty body."""
        response = client.put("/tasks/507f1f77bcf86cd799439011", json={})

        assert response.status_code == 400
        assert "At least one field must be provided" in response.json()["detail"]

    def test_delete_task(self, mock_task_model):
        """Test deleting a task."""
        mock_task_model.delete_task.return_value = True

        response = client.delete("/tasks/507f1f77bcf86cd799439011")

        assert response.status_code == 204

    def test_delete_task_not_found(self, mock_task_model):
        """Test deleting non-existent task."""
        mock_task_model.delete_task.return_value = False

        response = client.delete("/tasks/507f1f77bcf86cd799439011")

        assert response.status_code == 404
        assert response.json() == {"detail": "Task not found"}

    def test_create_task_validation_error(self):
        """Test validation errors."""
        # Empty title
        response = client.post("/tasks/", json={"title": ""})
        assert response.status_code == 422

        # Title too long
        response = client.post("/tasks/", json={"title": "x" * 101})
        assert response.status_code == 422

        # Description too long
        response = client.post(
            "/tasks/", json={"title": "Test", "description": "x" * 501}
        )
        assert response.status_code == 422
