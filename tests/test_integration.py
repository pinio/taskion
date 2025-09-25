import pytest
from fastapi.testclient import TestClient
import tempfile
import os
import shutil

from app import app

client = TestClient(app)


@pytest.fixture(scope="function")
def temp_db():
    """Create a temporary database for integration testing."""
    temp_dir = tempfile.mkdtemp()
    db_path = os.path.join(temp_dir, "test_db")

    # Patch the TaskModel to use temporary database
    from unittest.mock import patch

    with patch("apps.tasks.routes.task_model") as mock_model:
        from apps.tasks.models import TaskModel

        real_model = TaskModel(db_path=db_path)
        mock_model.create_task = real_model.create_task
        mock_model.get_task_by_id = real_model.get_task_by_id
        mock_model.get_tasks = real_model.get_tasks
        mock_model.update_task = real_model.update_task
        mock_model.delete_task = real_model.delete_task

        yield real_model

    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_complete_task_lifecycle(temp_db):
    """Test complete task lifecycle with real database."""
    # Create task
    create_response = client.post(
        "/tasks/",
        json={"title": "Integration Test Task", "description": "Test description"},
    )

    assert create_response.status_code == 201
    task_data = create_response.json()
    task_id = task_data["id"]

    # Get task by ID
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 200
    retrieved_task = get_response.json()
    assert retrieved_task["title"] == "Integration Test Task"

    # Update task
    update_response = client.put(
        f"/tasks/{task_id}", json={"title": "Updated Task", "done": True}
    )
    assert update_response.status_code == 200
    updated_task = update_response.json()
    assert updated_task["title"] == "Updated Task"
    assert updated_task["done"] is True

    # Delete task
    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 204

    # Verify deletion
    get_deleted_response = client.get(f"/tasks/{task_id}")
    assert get_deleted_response.status_code == 404


def test_task_filtering_and_pagination(temp_db):
    """Test task filtering and pagination."""
    # Create multiple tasks
    task_ids = []
    for i in range(5):
        response = client.post(
            "/tasks/", json={"title": f"Task {i + 1}", "done": i % 2 == 0}
        )
        assert response.status_code == 201
        task_ids.append(response.json()["id"])

    # Test pagination
    page1 = client.get("/tasks/?limit=3&offset=0")
    assert page1.status_code == 200
    assert len(page1.json()) == 3

    page2 = client.get("/tasks/?limit=3&offset=3")
    assert page2.status_code == 200
    assert len(page2.json()) == 2

    # Test filtering
    done_tasks = client.get("/tasks/?done=true")
    assert done_tasks.status_code == 200
    assert len(done_tasks.json()) == 3  # Tasks 1, 3, 5

    pending_tasks = client.get("/tasks/?done=false")
    assert pending_tasks.status_code == 200
    assert len(pending_tasks.json()) == 2  # Tasks 2, 4
