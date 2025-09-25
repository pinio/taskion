import pytest
from pydantic import ValidationError
from datetime import datetime
from unittest.mock import Mock, patch

from apps.tasks.requests import TaskCreate, TaskUpdate
from apps.tasks.responses import TaskOut
from apps.tasks.models import TaskModel


class TestTaskCreateModel:
    """Test TaskCreate Pydantic model."""

    def test_valid_task_create(self):
        """Test valid task creation."""
        task = TaskCreate(title="Test Task", description="Test Description")
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.done is False

    def test_task_create_minimal(self):
        """Test task with only title."""
        task = TaskCreate(title="Test Task")
        assert task.title == "Test Task"
        assert task.description is None
        assert task.done is False

    def test_task_create_validation_errors(self):
        """Test validation errors."""
        # Empty title
        with pytest.raises(ValidationError):
            TaskCreate(title="")

        # Title too long
        with pytest.raises(ValidationError):
            TaskCreate(title="x" * 101)

        # Description too long
        with pytest.raises(ValidationError):
            TaskCreate(title="Test", description="x" * 501)


class TestTaskUpdateModel:
    """Test TaskUpdate Pydantic model."""

    def test_valid_task_update(self):
        """Test valid task update."""
        task = TaskUpdate(title="Updated Task", done=True)
        assert task.title == "Updated Task"
        assert task.done is True
        assert task.has_updates() is True

    def test_empty_task_update(self):
        """Test empty update."""
        task = TaskUpdate()
        assert task.has_updates() is False

    def test_task_update_validation_errors(self):
        """Test validation errors."""
        # Empty title
        with pytest.raises(ValidationError):
            TaskUpdate(title="")

        # Title too long
        with pytest.raises(ValidationError):
            TaskUpdate(title="x" * 101)


class TestTaskOutModel:
    """Test TaskOut Pydantic model."""

    def test_task_out_creation(self):
        """Test TaskOut model creation."""
        now = datetime.utcnow()
        task = TaskOut(
            id="507f1f77bcf86cd799439011",
            title="Test Task",
            description="Test Description",
            done=False,
            created_at=now,
            updated_at=now,
        )

        assert task.id == "507f1f77bcf86cd799439011"
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.done is False
        assert task.created_at == now
        assert task.updated_at == now


class TestTaskDatabaseModel:
    """Test TaskModel database operations."""

    @patch("apps.tasks.models.MontyClient")
    def test_create_task(self, mock_client):
        """Test database task creation."""
        # Setup mocks
        mock_collection = Mock()
        mock_client.return_value.todo.tasks = mock_collection

        model = TaskModel("test_db")

        with patch("apps.tasks.models.ObjectId") as mock_objectid, patch(
            "apps.tasks.models.datetime"
        ) as mock_datetime:
            mock_objectid.return_value = "507f1f77bcf86cd799439011"
            now = datetime(2023, 1, 1, 12, 0, 0)
            mock_datetime.utcnow.return_value = now

            result = model.create_task("Test Task", "Test Description", False)

            assert result["id"] == "507f1f77bcf86cd799439011"
            assert result["title"] == "Test Task"
            assert result["description"] == "Test Description"
            assert result["done"] is False
            assert result["created_at"] == now
            assert result["updated_at"] == now

    @patch("apps.tasks.models.MontyClient")
    def test_get_task_by_id(self, mock_client):
        """Test getting task by ID."""
        mock_collection = Mock()
        mock_client.return_value.todo.tasks = mock_collection

        task_data = {
            "_id": "507f1f77bcf86cd799439011",
            "title": "Test Task",
            "description": "Test Description",
            "done": False,
            "created_at": datetime(2023, 1, 1),
            "updated_at": datetime(2023, 1, 1),
        }
        mock_collection.find_one.return_value = task_data

        model = TaskModel("test_db")
        result = model.get_task_by_id("507f1f77bcf86cd799439011")

        assert result["id"] == "507f1f77bcf86cd799439011"
        assert result["title"] == "Test Task"
