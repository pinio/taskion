from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response

from .models import TaskModel
from .requests import TaskCreate, TaskUpdate
from .responses import TaskOut

router = APIRouter(prefix="/tasks", tags=["tasks"])

# Initialize the database model
task_model = TaskModel()


@router.post("/", response_model=TaskOut, status_code=201)
async def create_task(task_data: TaskCreate):
    """Create a new task."""
    task = task_model.create_task(
        title=task_data.title, description=task_data.description, done=task_data.done
    )
    return TaskOut(**task)


@router.get("/", response_model=List[TaskOut])
async def get_tasks(
    done: Optional[bool] = Query(None, description="Filter by completion status"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of tasks"),
    offset: int = Query(0, ge=0, description="Number of tasks to skip"),
):
    """Get all tasks with optional filtering."""
    tasks = task_model.get_tasks(done=done, limit=limit, offset=offset)
    return [TaskOut(**task) for task in tasks]


@router.get("/{task_id}", response_model=TaskOut)
async def get_task(task_id: str):
    """Get a specific task by ID."""
    task = task_model.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskOut(**task)


@router.put("/{task_id}", response_model=TaskOut)
async def update_task(task_id: str, task_update: TaskUpdate):
    """Update a task."""
    # Check if the update has any data
    if not task_update.has_updates():
        raise HTTPException(
            status_code=400, detail="At least one field must be provided for update"
        )

    updated_task = task_model.update_task(
        task_id=task_id,
        title=task_update.title,
        description=task_update.description,
        done=task_update.done,
    )

    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return TaskOut(**updated_task)


@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: str):
    """Delete a task."""
    success = task_model.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return Response(status_code=204)
