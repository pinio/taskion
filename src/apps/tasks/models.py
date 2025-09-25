from datetime import datetime
from typing import Dict, List, Optional

from bson import ObjectId
from montydb import MontyClient


class TaskModel:
    """Database model for tasks using MontyDB."""

    def __init__(self, db_path: str = "todo_db"):
        """Initialize the database connection."""
        self.client = MontyClient(db_path)
        self.db = self.client.todo
        self.collection = self.db.tasks

    def create_task(
        self, title: str, description: Optional[str] = None, done: bool = False
    ) -> Dict:
        """Create a new task."""
        now = datetime.utcnow()
        task_data = {
            "_id": str(ObjectId()),
            "title": title,
            "description": description,
            "done": done,
            "created_at": now,
            "updated_at": now,
        }

        self.collection.insert_one(task_data)
        return self._format_task(task_data)

    def get_task_by_id(self, task_id: str) -> Optional[Dict]:
        """Get a task by its ID."""
        task = self.collection.find_one({"_id": task_id})
        if task:
            return self._format_task(task)
        return None

    def get_tasks(
        self, done: Optional[bool] = None, limit: int = 20, offset: int = 0
    ) -> List[Dict]:
        """Get tasks with optional filtering."""
        query = {}
        if done is not None:
            query["done"] = done

        tasks = (
            self.collection.find(query).sort("created_at", -1).skip(offset).limit(limit)
        )

        return [self._format_task(task) for task in tasks]

    def update_task(
        self,
        task_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        done: Optional[bool] = None,
    ) -> Optional[Dict]:
        """Update a task."""
        # Check if task exists
        if not self.collection.find_one({"_id": task_id}):
            return None

        update_data = {"updated_at": datetime.utcnow()}

        if title is not None:
            update_data["title"] = title
        if description is not None:
            update_data["description"] = description
        if done is not None:
            update_data["done"] = done

        self.collection.update_one({"_id": task_id}, {"$set": update_data})

        updated_task = self.collection.find_one({"_id": task_id})
        return self._format_task(updated_task) if updated_task else None

    def delete_task(self, task_id: str) -> bool:
        """Delete a task."""
        result = self.collection.delete_one({"_id": task_id})
        return result.deleted_count > 0

    def _format_task(self, task: Dict) -> Dict:
        """Format task data for API response."""
        return {
            "id": task["_id"],
            "title": task["title"],
            "description": task["description"],
            "done": task["done"],
            "created_at": task["created_at"],
            "updated_at": task["updated_at"],
        }
